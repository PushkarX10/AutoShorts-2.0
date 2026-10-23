"""
AutoShorts 2.0 — Audio Timeline Mixer.

Synchronizes and mixes all voice audio clips, typing sounds, bubble pops,
punchline accents, and background music into a single master audio track.
"""
from __future__ import annotations

import subprocess
import wave
from pathlib import Path
from typing import Optional

import numpy as np
from rich.console import Console

from src.audio.sfx_generator import ensure_default_audio_assets, SAMPLE_RATE
from src.config.settings import get, get_temp_dir
from src.models.schemas import AudioManifest, Timeline

console = Console()


def _read_wav_to_float(path: Path | str, target_sr: int = SAMPLE_RATE) -> np.ndarray:
    """Read a WAV file and return float samples (-1.0 to 1.0) as 2D array (samples, channels)."""
    with wave.open(str(path), "rb") as wf:
        n_channels = wf.getnchannels()
        samp_width = wf.getsampwidth()
        framerate = wf.getframerate()
        n_frames = wf.getnframes()
        raw = wf.readframes(n_frames)

    if samp_width == 2:
        dtype = np.int16
        scale = 32768.0
    elif samp_width == 4:
        dtype = np.int32
        scale = 2147483648.0
    elif samp_width == 1:
        dtype = np.uint8
        # Convert uint8 to float
        arr = np.frombuffer(raw, dtype=dtype).astype(np.float32)
        arr = (arr - 128.0) / 128.0
        if n_channels > 1:
            arr = arr.reshape(-1, n_channels)
        else:
            arr = arr.reshape(-1, 1)
        return arr
    else:
        raise ValueError(f"Unsupported sample width: {samp_width}")

    arr = np.frombuffer(raw, dtype=dtype).astype(np.float32) / scale
    if n_channels > 1:
        arr = arr.reshape(-1, n_channels)
    else:
        arr = arr.reshape(-1, 1)

    # Resample if sample rate doesn't match
    if framerate != target_sr and len(arr) > 0:
        new_len = int(len(arr) * target_sr / framerate)
        # Linear interpolation per channel
        orig_indices = np.linspace(0, len(arr) - 1, len(arr))
        new_indices = np.linspace(0, len(arr) - 1, new_len)
        resampled = np.zeros((new_len, n_channels), dtype=np.float32)
        for ch in range(n_channels):
            resampled[:, ch] = np.interp(new_indices, orig_indices, arr[:, ch])
        arr = resampled

    return arr


def _write_float_to_wav(
    samples: np.ndarray,
    output_path: Path,
    sample_rate: int = SAMPLE_RATE,
) -> Path:
    """Write 2D float samples (samples, channels) to 16-bit PCM WAV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    # Ensure 2D
    if samples.ndim == 1:
        samples = samples.reshape(-1, 1)

    # If mono, convert to stereo
    if samples.shape[1] == 1:
        samples = np.repeat(samples, 2, axis=1)

    # Soft peak limiting
    peak = np.max(np.abs(samples))
    if peak > 0.95:
        # Soft tanh limiter
        samples = np.tanh(samples / peak * 1.2) * 0.95
    else:
        samples = np.clip(samples, -0.98, 0.98)

    int_samples = (samples * 32767).astype(np.int16)

    with wave.open(str(output_path), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(int_samples.tobytes())

    return output_path


def mix_master_audio(
    timeline: Timeline,
    audio_manifest: AudioManifest,
    output_path: Path | None = None,
) -> Path:
    """
    Mix voices, SFX, and background music into a master audio file.
    Accurately places all clips according to timeline.events timestamps.
    """
    if output_path is None:
        output_path = get_temp_dir() / "master_audio.wav"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    audio_cfg = get("audio", default={})
    voice_vol = audio_cfg.get("voice_volume", 1.0)
    music_vol = audio_cfg.get("music_volume", 0.12)
    sfx_vol = audio_cfg.get("sfx_volume", 0.28)
    normalize_loudness = audio_cfg.get("normalize_loudness", True)
    target_lufs = audio_cfg.get("target_loudness_lufs", -14)

    total_duration = timeline.total_duration_sec
    total_samples = int(total_duration * SAMPLE_RATE)

    # Allocate stereo master buffers
    master_voice = np.zeros((total_samples, 2), dtype=np.float32)
    master_sfx = np.zeros((total_samples, 2), dtype=np.float32)
    master_bgm = np.zeros((total_samples, 2), dtype=np.float32)

    # 1. Load sound assets
    sfx_assets = ensure_default_audio_assets()
    pop_sound = _read_wav_to_float(sfx_assets["pop"])
    typing_sound = _read_wav_to_float(sfx_assets["typing"])
    punchline_sound = _read_wav_to_float(sfx_assets["punchline"])
    whoosh_sound = _read_wav_to_float(sfx_assets["whoosh"])

    # 2. Place Voices and SFX according to timeline
    for event in timeline.events:
        # Voice clip
        clip = audio_manifest.get_clip(event.message_id)
        if clip and Path(clip.audio_path).exists():
            v_samples = _read_wav_to_float(clip.audio_path)
            start_idx = int(event.voice_start_sec * SAMPLE_RATE)
            end_idx = min(start_idx + len(v_samples), total_samples)
            copy_len = end_idx - start_idx
            if copy_len > 0:
                if v_samples.shape[1] == 1:
                    master_voice[start_idx:end_idx, 0] += v_samples[:copy_len, 0]
                    master_voice[start_idx:end_idx, 1] += v_samples[:copy_len, 0]
                else:
                    master_voice[start_idx:end_idx] += v_samples[:copy_len, :2]

        # Bubble Pop SFX at bubble appearance
        pop_start = int(event.bubble_appear_sec * SAMPLE_RATE)
        pop_len = min(len(pop_sound), total_samples - pop_start)
        if pop_start >= 0 and pop_len > 0:
            if pop_sound.shape[1] == 1:
                master_sfx[pop_start : pop_start + pop_len, 0] += pop_sound[:pop_len, 0]
                master_sfx[pop_start : pop_start + pop_len, 1] += pop_sound[:pop_len, 0]
            else:
                master_sfx[pop_start : pop_start + pop_len] += pop_sound[:pop_len, :2]

        # Typing SFX during typing window (soft clicks spaced ~130ms apart)
        if event.typing_start_sec < event.typing_end_sec:
            t_curr = event.typing_start_sec + 0.05
            while t_curr < event.typing_end_sec:
                t_idx = int(t_curr * SAMPLE_RATE)
                c_len = min(len(typing_sound), total_samples - t_idx)
                if t_idx >= 0 and c_len > 0:
                    gain = 0.5
                    if typing_sound.shape[1] == 1:
                        master_sfx[t_idx : t_idx + c_len, 0] += typing_sound[:c_len, 0] * gain
                        master_sfx[t_idx : t_idx + c_len, 1] += typing_sound[:c_len, 0] * gain
                    else:
                        master_sfx[t_idx : t_idx + c_len] += typing_sound[:c_len, :2] * gain
                t_curr += 0.13

        # Punchline sting
        if event.is_punchline:
            sting_start = int((event.bubble_appear_sec + 0.05) * SAMPLE_RATE)
            s_len = min(len(punchline_sound), total_samples - sting_start)
            if sting_start >= 0 and s_len > 0:
                if punchline_sound.shape[1] == 1:
                    master_sfx[sting_start : sting_start + s_len, 0] += punchline_sound[:s_len, 0] * 0.7
                    master_sfx[sting_start : sting_start + s_len, 1] += punchline_sound[:s_len, 0] * 0.7
                else:
                    master_sfx[sting_start : sting_start + s_len] += punchline_sound[:s_len, :2] * 0.7

    # 3. Add Background Music (looping with smooth fade-in and fade-out)
    if "music" in sfx_assets and Path(sfx_assets["music"]).exists():
        bgm_raw = _read_wav_to_float(sfx_assets["music"])
        if len(bgm_raw) > 0:
            bgm_len = len(bgm_raw)
            # Tile BGM across total_samples
            n_repeats = (total_samples // bgm_len) + 1
            tiled_bgm = np.tile(bgm_raw, (n_repeats, 1))[:total_samples]
            if tiled_bgm.shape[1] == 1:
                tiled_bgm = np.repeat(tiled_bgm, 2, axis=1)

            # Apply smooth 1s fade-in and 1.5s fade-out
            fade_in_len = min(int(1.0 * SAMPLE_RATE), total_samples)
            fade_out_len = min(int(1.5 * SAMPLE_RATE), total_samples)
            fade_curve_in = np.linspace(0, 1, fade_in_len)[:, None]
            fade_curve_out = np.linspace(1, 0, fade_out_len)[:, None]

            tiled_bgm[:fade_in_len] *= fade_curve_in
            tiled_bgm[-fade_out_len:] *= fade_curve_out

            master_bgm = tiled_bgm[:, :2]

    # 4. Sum with volume weightings
    master = (
        master_voice * voice_vol
        + master_sfx * sfx_vol
        + master_bgm * music_vol
    )

    # 5. Export raw mixed WAV
    raw_mix_path = output_path.with_name("raw_mix.wav")
    _write_float_to_wav(master, raw_mix_path)

    # 6. Apply loudness normalization via FFmpeg loudnorm if requested
    if normalize_loudness:
        try:
            norm_cmd = [
                "ffmpeg", "-y",
                "-i", str(raw_mix_path),
                "-af", f"loudnorm=I={target_lufs}:TP=-1.5:LRA=11",
                "-ar", str(SAMPLE_RATE),
                "-ac", "2",
                str(output_path),
            ]
            res = subprocess.run(norm_cmd, capture_output=True, text=True, timeout=60)
            if res.returncode == 0 and output_path.exists() and output_path.stat().st_size > 1000:
                raw_mix_path.unlink(missing_ok=True)
                console.print(f"[green]✓[/green] Audio master mixed and normalized to {target_lufs} LUFS")
                return output_path
        except Exception as e:
            console.print(f"[yellow]⚠[/yellow] Loudnorm failed ({e}), using raw mix")

    # Fallback to raw mix if normalization skipped or failed
    if raw_mix_path.exists():
        raw_mix_path.replace(output_path)

    console.print(f"[green]✓[/green] Audio master mixed: {output_path.name}")
    return output_path
