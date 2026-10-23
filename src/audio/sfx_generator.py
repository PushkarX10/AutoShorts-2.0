"""
AutoShorts 2.0 — Sound Effects & Music Generator.

Provides procedural generation of clean sound effects (pop, typing, punchline, whoosh)
and background music tracks if custom files are not present in assets/.
"""
from __future__ import annotations

import math
import struct
import wave
from pathlib import Path
from typing import Optional

import numpy as np
from rich.console import Console

from src.config.settings import get_project_root

console = Console()

SAMPLE_RATE = 44100


def _save_wav(
    samples: np.ndarray,
    output_path: Path,
    sample_rate: int = SAMPLE_RATE,
    channels: int = 1,
) -> Path:
    """Save float numpy array (-1.0 to 1.0) as 16-bit PCM WAV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    # Clip and convert to int16
    samples = np.clip(samples, -0.98, 0.98)
    int_samples = (samples * 32767).astype(np.int16)

    with wave.open(str(output_path), "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        if channels == 1:
            wf.writeframes(int_samples.tobytes())
        else:
            wf.writeframes(int_samples.tobytes())
    return output_path


def generate_bubble_pop(output_path: Path) -> Path:
    """
    Generate a clean, pleasant chat bubble pop sound (65 ms).
    Sine frequency drops quickly from 850 Hz to 240 Hz with fast exponential decay.
    """
    duration = 0.065
    n_samples = int(duration * SAMPLE_RATE)
    t = np.linspace(0, duration, n_samples, endpoint=False)

    # Downward pitch sweep
    freq = 850.0 * np.exp(-t * 22.0) + 240.0
    phase = 2.0 * np.pi * np.cumsum(freq) / SAMPLE_RATE

    # Amplitude envelope: quick attack (3ms), exponential decay
    attack_samples = int(0.003 * SAMPLE_RATE)
    envelope = np.exp(-t * 55.0)
    envelope[:attack_samples] = np.linspace(0, 1, attack_samples)

    # High harmonic for crispness
    waveform = np.sin(phase) * 0.85 + np.sin(phase * 2.2) * 0.15
    audio = waveform * envelope * 0.9

    return _save_wav(audio, output_path)


def generate_typing_click(output_path: Path) -> Path:
    """
    Generate a subtle, soft mechanical typing tap sound (35 ms).
    """
    duration = 0.035
    n_samples = int(duration * SAMPLE_RATE)
    t = np.linspace(0, duration, n_samples, endpoint=False)

    # Click resonance at ~1800 Hz and 3200 Hz
    wave1 = np.sin(2.0 * np.pi * 1800.0 * t) * 0.6
    wave2 = np.sin(2.0 * np.pi * 3200.0 * t) * 0.3
    # Subtle burst of shaped white noise
    noise = np.random.uniform(-0.15, 0.15, n_samples)

    envelope = np.exp(-t * 130.0)
    envelope[: int(0.002 * SAMPLE_RATE)] = np.linspace(0, 1, int(0.002 * SAMPLE_RATE))

    audio = (wave1 + wave2 + noise) * envelope * 0.6
    return _save_wav(audio, output_path)


def generate_punchline_sting(output_path: Path) -> Path:
    """
    Generate a bright, comedic punchline chime / marimba accent (0.75 s).
    Ascending bright triad with sparkle and smooth fade.
    """
    duration = 0.75
    n_samples = int(duration * SAMPLE_RATE)
    audio = np.zeros(n_samples, dtype=np.float64)

    # 3 notes: C6 (1046.5 Hz), E6 (1318.5 Hz), G6 (1567.98 Hz), followed by high C7 (2093 Hz)
    notes = [
        (0.00, 1046.50, 0.60),
        (0.08, 1318.51, 0.70),
        (0.16, 1567.98, 0.85),
        (0.24, 2093.00, 0.95),
    ]

    for start_t, freq, amp in notes:
        start_idx = int(start_t * SAMPLE_RATE)
        rem_samples = n_samples - start_idx
        if rem_samples <= 0:
            continue
        t_note = np.linspace(0, rem_samples / SAMPLE_RATE, rem_samples, endpoint=False)
        env = np.exp(-t_note * 8.0)
        attack_len = min(int(0.005 * SAMPLE_RATE), rem_samples)
        env[:attack_len] = np.linspace(0, 1, attack_len)

        note_wave = (
            np.sin(2.0 * np.pi * freq * t_note) * 0.7
            + np.sin(2.0 * np.pi * freq * 2.0 * t_note) * 0.25
            + np.sin(2.0 * np.pi * freq * 3.0 * t_note) * 0.05
        )
        audio[start_idx:] += note_wave * env * amp

    audio = audio / max(np.max(np.abs(audio)), 1e-6) * 0.85
    return _save_wav(audio, output_path)


def generate_whoosh(output_path: Path) -> Path:
    """
    Generate a gentle, smooth air whoosh sound for scrolling (0.18 s).
    """
    duration = 0.18
    n_samples = int(duration * SAMPLE_RATE)
    t = np.linspace(0, duration, n_samples, endpoint=False)

    noise = np.random.uniform(-1.0, 1.0, n_samples)
    # Sine sweep modulator
    sweep = np.sin(np.pi * (t / duration)) ** 2
    carrier = np.sin(2.0 * np.pi * (350.0 + 400.0 * np.sin(np.pi * t / duration)) * t)

    audio = (noise * 0.6 + carrier * 0.4) * sweep * 0.45
    return _save_wav(audio, output_path)


def generate_chill_bgm(output_path: Path, duration: float = 60.0) -> Path:
    """
    Generate a smooth, chill, non-intrusive background beat with warm electric piano chords
    and soft rhythm (stereo 44.1kHz).
    """
    n_samples = int(duration * SAMPLE_RATE)
    left = np.zeros(n_samples, dtype=np.float64)
    right = np.zeros(n_samples, dtype=np.float64)

    # Chord progression (Fmaj7 - Em7 - Dm7 - Cmaj7)
    # 4 beats per chord, 85 BPM
    bpm = 85.0
    beat_dur = 60.0 / bpm
    bar_dur = beat_dur * 4.0

    chord_freqs = [
        [174.61, 220.00, 261.63, 329.63],  # Fmaj7 (F3, A3, C4, E4)
        [164.81, 196.00, 246.94, 293.66],  # Em7   (E3, G3, B3, D4)
        [146.83, 174.61, 220.00, 261.63],  # Dm7   (D3, F3, A3, C4)
        [130.81, 164.81, 196.00, 246.94],  # Cmaj7 (C3, E3, G3, B3)
    ]

    # Warm Rhodes-like synth chord synthesizer
    cur_t = 0.0
    chord_idx = 0
    while cur_t < duration:
        chord = chord_freqs[chord_idx % len(chord_freqs)]
        chord_samples = int(min(bar_dur, duration - cur_t) * SAMPLE_RATE)
        t_chord = np.linspace(0, chord_samples / SAMPLE_RATE, chord_samples, endpoint=False)
        start_idx = int(cur_t * SAMPLE_RATE)
        end_idx = start_idx + chord_samples

        env = np.exp(-t_chord * 0.8) * (1.0 - np.exp(-t_chord * 30.0))

        chord_signal_l = np.zeros(chord_samples, dtype=np.float64)
        chord_signal_r = np.zeros(chord_samples, dtype=np.float64)

        for i, f in enumerate(chord):
            # Gentle vibrato / tremolo
            mod = 1.0 + 0.008 * np.sin(2.0 * np.pi * 4.5 * t_chord)
            tone = (
                np.sin(2.0 * np.pi * f * mod * t_chord) * 0.6
                + np.sin(2.0 * np.pi * f * 2.0 * t_chord) * 0.25
                + np.sin(2.0 * np.pi * f * 3.0 * t_chord) * 0.08
            )
            # Stereo panning spread across chord voices
            pan = (i / (len(chord) - 1)) if len(chord) > 1 else 0.5
            chord_signal_l += tone * (1.0 - pan * 0.5)
            chord_signal_r += tone * (0.5 + pan * 0.5)

        left[start_idx:end_idx] += chord_signal_l * env * 0.35
        right[start_idx:end_idx] += chord_signal_r * env * 0.35

        cur_t += bar_dur
        chord_idx += 1

    # Add gentle soft lo-fi rhythm (kick on 1 and 3, soft rim/click on 2 and 4, light shaker)
    cur_beat = 0.0
    beat_count = 0
    while cur_beat < duration:
        start_idx = int(cur_beat * SAMPLE_RATE)
        rem = n_samples - start_idx
        if rem <= 0:
            break

        is_kick = (beat_count % 4 == 0) or (beat_count % 4 == 2 and (beat_count % 8 == 2))
        is_snare = (beat_count % 4 == 1) or (beat_count % 4 == 3)

        if is_kick:
            k_len = min(int(0.12 * SAMPLE_RATE), rem)
            t_k = np.linspace(0, k_len / SAMPLE_RATE, k_len, endpoint=False)
            k_freq = 110.0 * np.exp(-t_k * 30.0) + 45.0
            k_wave = np.sin(2.0 * np.pi * np.cumsum(k_freq) / SAMPLE_RATE) * np.exp(-t_k * 18.0) * 0.35
            left[start_idx : start_idx + k_len] += k_wave
            right[start_idx : start_idx + k_len] += k_wave

        if is_snare:
            s_len = min(int(0.06 * SAMPLE_RATE), rem)
            t_s = np.linspace(0, s_len / SAMPLE_RATE, s_len, endpoint=False)
            noise_s = np.random.uniform(-0.15, 0.15, s_len) * np.exp(-t_s * 40.0)
            left[start_idx : start_idx + s_len] += noise_s
            right[start_idx : start_idx + s_len] += noise_s

        # Light hihat / shaker on every eighth note
        hat_len = min(int(0.02 * SAMPLE_RATE), rem)
        t_h = np.linspace(0, hat_len / SAMPLE_RATE, hat_len, endpoint=False)
        hat = np.random.uniform(-0.06, 0.06, hat_len) * np.exp(-t_h * 120.0)
        left[start_idx : start_idx + hat_len] += hat * 0.4
        right[start_idx : start_idx + hat_len] += hat * 0.6

        cur_beat += beat_dur
        beat_count += 1

    # Interleave stereo
    stereo = np.column_stack((left, right))
    max_val = np.max(np.abs(stereo))
    if max_val > 0:
        stereo = stereo / max_val * 0.75

    output_path.parent.mkdir(parents=True, exist_ok=True)
    int_stereo = (np.clip(stereo, -0.98, 0.98) * 32767).astype(np.int16)
    with wave.open(str(output_path), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(int_stereo.tobytes())

    return output_path


def ensure_default_audio_assets() -> dict[str, Path]:
    """
    Ensure all default sound effects and background music exist.
    If assets are not present in assets/, generates clean procedural versions.
    Returns dictionary mapping asset names to paths.
    """
    root = get_project_root()
    sfx_dir = root / "assets" / "sound_effects"
    music_dir = root / "assets" / "music"
    sfx_dir.mkdir(parents=True, exist_ok=True)
    music_dir.mkdir(parents=True, exist_ok=True)

    assets: dict[str, Path] = {}

    # Pop sound
    pop_candidates = list(sfx_dir.glob("pop*.wav")) + list(sfx_dir.glob("bubble*.wav"))
    if pop_candidates:
        assets["pop"] = pop_candidates[0]
    else:
        pop_path = sfx_dir / "bubble_pop.wav"
        generate_bubble_pop(pop_path)
        assets["pop"] = pop_path

    # Typing sound
    type_candidates = list(sfx_dir.glob("typing*.wav")) + list(sfx_dir.glob("click*.wav"))
    if type_candidates:
        assets["typing"] = type_candidates[0]
    else:
        type_path = sfx_dir / "typing_click.wav"
        generate_typing_click(type_path)
        assets["typing"] = type_path

    # Punchline sting
    sting_candidates = list(sfx_dir.glob("punchline*.wav")) + list(sfx_dir.glob("sting*.wav"))
    if sting_candidates:
        assets["punchline"] = sting_candidates[0]
    else:
        sting_path = sfx_dir / "punchline_sting.wav"
        generate_punchline_sting(sting_path)
        assets["punchline"] = sting_path

    # Whoosh sound
    whoosh_candidates = list(sfx_dir.glob("whoosh*.wav"))
    if whoosh_candidates:
        assets["whoosh"] = whoosh_candidates[0]
    else:
        whoosh_path = sfx_dir / "whoosh.wav"
        generate_whoosh(whoosh_path)
        assets["whoosh"] = whoosh_path

    # Background music
    bgm_candidates = list(music_dir.glob("*.mp3")) + list(music_dir.glob("*.wav"))
    if bgm_candidates:
        assets["music"] = bgm_candidates[0]
    else:
        bgm_path = music_dir / "chill_bgm.wav"
        generate_chill_bgm(bgm_path, duration=60.0)
        assets["music"] = bgm_path

    return assets
