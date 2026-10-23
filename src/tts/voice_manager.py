"""
AutoShorts 2.0 — Voice Manager.

Maps characters to TTS voices and manages voice configuration.
"""
from __future__ import annotations

from rich.console import Console

from src.config.settings import get_available_voices
from src.models.schemas import Character, Conversation, Emotion

console = Console()

# Emotion-to-TTS rate/pitch modifiers for edge-tts
EMOTION_MODIFIERS: dict[Emotion, dict[str, str]] = {
    Emotion.CASUAL:      {"rate": "+0%",  "pitch": "+0Hz"},
    Emotion.CONFUSED:    {"rate": "-5%",  "pitch": "+3Hz"},
    Emotion.EXCITED:     {"rate": "+12%", "pitch": "+5Hz"},
    Emotion.SARCASTIC:   {"rate": "-3%",  "pitch": "-2Hz"},
    Emotion.EMBARRASSED: {"rate": "-8%",  "pitch": "+2Hz"},
    Emotion.ANGRY:       {"rate": "+8%",  "pitch": "-3Hz"},
    Emotion.LAUGHING:    {"rate": "+5%",  "pitch": "+4Hz"},
    Emotion.SHOCKED:     {"rate": "+10%", "pitch": "+6Hz"},
    Emotion.NERVOUS:     {"rate": "+3%",  "pitch": "+3Hz"},
    Emotion.PROUD:       {"rate": "-2%",  "pitch": "-1Hz"},
}


class VoiceProfile:
    """Resolved voice settings for a character."""

    def __init__(self, voice_id: str, edge_voice: str, base_rate: str, base_pitch: str, base_volume: str):
        self.voice_id = voice_id
        self.edge_voice = edge_voice
        self.base_rate = base_rate
        self.base_pitch = base_pitch
        self.base_volume = base_volume

    def get_params(self, emotion: Emotion = Emotion.CASUAL) -> dict[str, str]:
        """Get edge-tts parameters with emotion modifiers applied."""
        mods = EMOTION_MODIFIERS.get(emotion, EMOTION_MODIFIERS[Emotion.CASUAL])

        rate = _combine_percentage(self.base_rate, mods["rate"])
        pitch = _combine_hz(self.base_pitch, mods["pitch"])

        return {
            "voice": self.edge_voice,
            "rate": rate,
            "pitch": pitch,
            "volume": self.base_volume,
        }


class VoiceManager:
    """Manages voice assignment and profiles for all characters."""

    def __init__(self):
        self.profiles: dict[str, VoiceProfile] = {}
        self._available = get_available_voices()

    def assign_voices(self, conversation: Conversation) -> dict[str, VoiceProfile]:
        """Assign a VoiceProfile to each character in the conversation."""
        self.profiles = {}

        for char in conversation.characters:
            voice_key = char.voice_id
            voice_cfg = self._available.get(voice_key, {})

            if not voice_cfg:
                # Fallback to first available voice
                fallback_key = list(self._available.keys())[0] if self._available else None
                if fallback_key:
                    voice_cfg = self._available[fallback_key]
                    console.print(f"[yellow]⚠[/yellow] Voice '{voice_key}' not found, "
                                  f"falling back to '{fallback_key}' for {char.name}")
                else:
                    voice_cfg = {"id": "en-US-JennyNeural", "rate": "+0%", "pitch": "+0Hz", "volume": "+0%"}
                    console.print(f"[yellow]⚠[/yellow] No voices configured, using default for {char.name}")

            profile = VoiceProfile(
                voice_id=voice_key,
                edge_voice=voice_cfg.get("id", "en-US-JennyNeural"),
                base_rate=voice_cfg.get("rate", "+0%"),
                base_pitch=voice_cfg.get("pitch", "+0Hz"),
                base_volume=voice_cfg.get("volume", "+0%"),
            )
            self.profiles[char.id] = profile
            console.print(f"  🎤 {char.name} → {profile.edge_voice}")

        return self.profiles

    def get_profile(self, character_id: str) -> VoiceProfile:
        """Get the voice profile for a character."""
        if character_id not in self.profiles:
            raise ValueError(f"No voice profile for character '{character_id}'")
        return self.profiles[character_id]


def _combine_percentage(base: str, modifier: str) -> str:
    """Combine two percentage strings: '+5%' + '+3%' = '+8%'."""
    base_val = _parse_pct(base)
    mod_val = _parse_pct(modifier)
    total = base_val + mod_val
    total = max(-50, min(50, total))  # clamp
    sign = "+" if total >= 0 else ""
    return f"{sign}{total}%"


def _combine_hz(base: str, modifier: str) -> str:
    """Combine two Hz strings: '+2Hz' + '+3Hz' = '+5Hz'."""
    base_val = _parse_hz(base)
    mod_val = _parse_hz(modifier)
    total = base_val + mod_val
    total = max(-20, min(20, total))
    sign = "+" if total >= 0 else ""
    return f"{sign}{total}Hz"


def _parse_pct(s: str) -> int:
    try:
        return int(s.replace("%", "").replace("+", ""))
    except (ValueError, AttributeError):
        return 0


def _parse_hz(s: str) -> int:
    try:
        return int(s.replace("Hz", "").replace("+", ""))
    except (ValueError, AttributeError):
        return 0
