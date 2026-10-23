"""
AutoShorts 2.0 — Speech Generator.

Generates one WAV audio file per message using edge-tts.
Measures actual durations and builds the AudioManifest.
"""
from __future__ import annotations

import asyncio
import json
import re
import subprocess
import struct
import wave
from pathlib import Path

import edge_tts
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

from src.config.settings import get_temp_dir
from src.models.schemas import AudioClip, AudioManifest, Conversation, Message
from src.tts.voice_manager import VoiceManager

console = Console()

EMOJI_PATTERN = re.compile(
    "["
    "\U0001f600-\U0001f64f"
    "\U0001f300-\U0001f5ff"
    "\U0001f680-\U0001f6ff"
    "\U0001f1e0-\U0001f1ff"
    "\U00002702-\U000027b0"
    "\U000024c2-\U0001f251"
    "\U0001f900-\U0001f9ff"
    "\U0001fa70-\U0001faff"
    "\U00002600-\U000026ff"
    "]+",
    flags=re.UNICODE,
)


def _clean_for_tts(text: str) -> str:
    """Strip emojis from text before feeding to TTS voice engine."""
    cleaned = EMOJI_PATTERN.sub("", text)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned if cleaned else text


async def _generate_single(
    message: Message,
    voice_manager: VoiceManager,
    output_dir: Path,
) -> AudioClip:
    """Generate TTS audio for a single message."""
    profile = voice_manager.get_profile(message.character_id)
    params = profile.get_params(message.emotion)

    mp3_path = output_dir / f"message_{message.id:03d}.mp3"
    wav_path = output_dir / f"message_{message.id:03d}.wav"
    if wav_path.exists() and wav_path.stat().st_size > 1000:
        duration = _get_wav_duration(wav_path)
        return AudioClip(
            message_id=message.id,
            character_id=message.character_id,
            text=message.text,
            audio_path=str(wav_path),
            duration_sec=round(duration, 3),
            voice_id=profile.voice_id,
        )

    # Clean emojis from TTS voice input while preserving in visual chat bubble
    tts_text = _clean_for_tts(message.text)

    # Generate with edge-tts
    communicate = edge_tts.Communicate(
        text=tts_text,
        voice=params["voice"],
        rate=params["rate"],
        pitch=params["pitch"],
        volume=params["volume"],
    )
    await communicate.save(str(mp3_path))

    if not mp3_path.exists() or mp3_path.stat().st_size < 100:
        raise RuntimeError(f"TTS failed for message {message.id}: empty output")

    # Convert MP3 → WAV using FFmpeg for accurate duration measurement
    _convert_to_wav(mp3_path, wav_path)

    # Measure actual duration
    duration = _get_wav_duration(wav_path)

    # Clean up MP3
    mp3_path.unlink(missing_ok=True)

    return AudioClip(
        message_id=message.id,
        character_id=message.character_id,
        text=message.text,
        audio_path=str(wav_path),
        duration_sec=round(duration, 3),
        voice_id=profile.voice_id,
    )


def generate_all_speech(
    conversation: Conversation,
    voice_manager: VoiceManager,
    output_dir: Path | None = None,
) -> AudioManifest:
    """
    Generate speech for every message in the conversation.
    Returns an AudioManifest with paths and durations.
    """
    if output_dir is None:
        output_dir = get_temp_dir() / "audio"
    output_dir.mkdir(parents=True, exist_ok=True)

    console.print(f"[cyan]⏳[/cyan] Generating speech for {len(conversation.messages)} messages…")

    # Assign voices
    voice_manager.assign_voices(conversation)

    # Generate all clips
    clips = asyncio.run(_generate_all_async(conversation, voice_manager, output_dir))

    total_duration = sum(c.duration_sec for c in clips)
    manifest = AudioManifest(clips=clips, total_voice_duration=round(total_duration, 3))

    # Save manifest to file for debugging / caching
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(manifest.model_dump_json(indent=2), encoding="utf-8")

    console.print(f"[green]✓[/green] Generated {len(clips)} audio clips, "
                  f"total voice duration: {total_duration:.1f}s")

    return manifest


async def _generate_all_async(
    conversation: Conversation,
    voice_manager: VoiceManager,
    output_dir: Path,
) -> list[AudioClip]:
    """Generate all clips, one at a time to avoid rate limiting."""
    clips: list[AudioClip] = []
    total = len(conversation.messages)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
        console=console,
    ) as progress:
        task = progress.add_task("Generating voices", total=total)

        for msg in conversation.messages:
            char = conversation.get_character(msg.character_id)
            char_name = char.name if char else msg.character_id

            try:
                clip = await _generate_single(msg, voice_manager, output_dir)
                clips.append(clip)
            except Exception as e:
                # Retry once
                console.print(f"[yellow]⚠[/yellow] Retry TTS for message {msg.id}: {e}")
                try:
                    await asyncio.sleep(1)
                    clip = await _generate_single(msg, voice_manager, output_dir)
                    clips.append(clip)
                except Exception as e2:
                    raise RuntimeError(
                        f"TTS failed for message {msg.id} ('{msg.text[:40]}…'): {e2}"
                    ) from e2

            progress.update(task, advance=1,
                          description=f"🎤 {char_name}: \"{msg.text[:30]}…\"")

    return clips


def _convert_to_wav(mp3_path: Path, wav_path: Path) -> None:
    """Convert MP3 to WAV using FFmpeg."""
    cmd = [
        "ffmpeg", "-y",
        "-i", str(mp3_path),
        "-acodec", "pcm_s16le",
        "-ar", "24000",
        "-ac", "1",
        str(wav_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if result.returncode != 0:
        raise RuntimeError(f"WAV conversion failed: {result.stderr[-500:]}")


def _get_wav_duration(wav_path: Path) -> float:
    """Get the duration of a WAV file in seconds."""
    try:
        with wave.open(str(wav_path), "rb") as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            if rate == 0:
                return 0.0
            return frames / float(rate)
    except Exception:
        # Fallback: use FFprobe
        return _get_duration_ffprobe(wav_path)


def _get_duration_ffprobe(path: Path) -> float:
    """Fallback duration measurement using FFprobe."""
    cmd = [
        "ffprobe", "-v", "quiet",
        "-show_entries", "format=duration",
        "-of", "json",
        str(path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    if result.returncode != 0:
        return 0.0
    try:
        data = json.loads(result.stdout)
        return float(data.get("format", {}).get("duration", 0))
    except (json.JSONDecodeError, ValueError):
        return 0.0
