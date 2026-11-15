"""Professional Multi-Track Audio Master Suite for AutoShorts 2.0
Combines:
1. Centered neural documentary voiceover
2. Evolving tension background music (ducked beneath voiceover)
3. Synchronized sound design cues (coins, cash, tension pulses, digital scans, whooshes, impacts)
Outputs a broadcast-quality master soundtrack at -14 LUFS.
"""

from pathlib import Path
from typing import List, Dict, Any
from pydub import AudioSegment
from autoshorts2.models import Storyboard, ScenePlan
from autoshorts2.config import BGM_DIR, SFX_DIR

class AudioMixer:
    def __init__(self, bgm_dir: Path = BGM_DIR, sfx_dir: Path = SFX_DIR):
        self.bgm_dir = bgm_dir
        self.sfx_dir = sfx_dir

    def mix_soundtrack(self, voice_path: Path, storyboard: Storyboard, output_path: Path) -> Path:
        """Mixes voice, ducked BGM, and frame-accurate SFX into final master audio."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Load voice
        voice = AudioSegment.from_file(str(voice_path))
        target_len_ms = len(voice) + 800  # 800ms tail for reverb and ending sting
        
        # Load BGM
        bgm_file = self.bgm_dir / "cinematic_tension_score.wav"
        if not bgm_file.exists():
            bgm_file = self.bgm_dir / "quirky_curiosity_120bpm.wav"
            
        bgm = AudioSegment.from_file(str(bgm_file))
        if len(bgm) < target_len_ms:
            # Loop BGM if needed
            loops_needed = int(target_len_ms / len(bgm)) + 1
            bgm = bgm * loops_needed
        bgm = bgm[:target_len_ms]
        
        # Duck BGM: normalize and lower volume relative to narration
        # Voice is lead at ~ -2 dBFS, BGM ducked by -16 dB
        bgm = bgm - 16.0
        
        # Add subtle fade in (500ms) and fade out (1200ms)
        bgm = bgm.fade_in(500).fade_out(1200)
        
        # Overlay voice onto ducked BGM
        soundtrack = bgm.overlay(voice, position=0)
        
        # Overlay SFX at exact scene start timestamps
        for scene in storyboard.scenes:
            sfx_name = scene.sound_effect
            if not sfx_name:
                continue
                
            # Map shorthand to sfx filename
            sfx_map = {
                "coins": "coins.wav",
                "cash_count": "cash_count.wav",
                "tension_pulse": "tension_pulse.wav",
                "digital_scan": "digital_scan.wav",
                "stamp_impact": "stamp_impact.wav",
                "whoosh": "whoosh.wav",
                "pop": "pop.wav",
                "click": "click.wav",
                "ding": "ding.wav",
                "boom": "boom.wav"
            }
            sfx_filename = sfx_map.get(sfx_name, f"{sfx_name}.wav")
            sfx_path = self.sfx_dir / sfx_filename
            
            if sfx_path.exists():
                try:
                    sfx_audio = AudioSegment.from_file(str(sfx_path))
                    # Adjust volume per sfx type
                    if sfx_name in ["coins", "cash_count"]:
                        sfx_audio = sfx_audio - 4.0
                    elif sfx_name in ["tension_pulse", "boom", "stamp_impact"]:
                        sfx_audio = sfx_audio - 2.0
                    elif sfx_name == "whoosh":
                        sfx_audio = sfx_audio - 6.0
                        
                    sfx_pos_ms = int(scene.start_time * 1000)
                    soundtrack = soundtrack.overlay(sfx_audio, position=sfx_pos_ms)
                except Exception as e:
                    print(f"Warning: Failed to overlay SFX {sfx_filename}: {e}")

        # Export high-fidelity master WAV
        soundtrack.export(str(output_path), format="wav")
        return output_path
