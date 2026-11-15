"""Procedural Cinematic Documentary Score Synthesizer for AutoShorts 2.0
Generates an evolving multi-stage cinematic background score:
- 0-10s: Subtle mystery (minimal sub drone + sparse Rhodes-like chime)
- 10-30s: Increasing tension (steady rhythmic kick/pulse + ticking clock texture)
- 30-50s: Analytical documentary (crisp synth arpeggio + filtered bass line)
- 50-65s: Climax tension (heavy sub bass + urgent syncopation)
- 65s+: Dramatic drop / silence followed by final impact sting
"""

import math
import struct
import wave
import random
from pathlib import Path

def generate_cinematic_score(output_file: Path, duration_sec: float = 75.0, sample_rate: int = 44100):
    total_samples = int(duration_sec * sample_rate)
    samples = [0.0] * total_samples
    
    # Fundamental tempo: 112 BPM (0.5357s per beat)
    beat_dur = 60.0 / 112.0
    total_beats = int(duration_sec / beat_dur)
    
    # 1. Sub-bass Drone (continuous with subtle pitch modulation)
    for i in range(total_samples):
        t = i / sample_rate
        # Silence at the dramatic drop (around 62s to 64s)
        if 62.0 <= t <= 64.2:
            continue
            
        # Modulating low bass (48Hz - 55Hz)
        bass_freq = 50.0 + 3.0 * math.sin(2 * math.pi * 0.15 * t)
        drone = math.sin(2 * math.pi * bass_freq * t)
        
        # Section intensity envelope
        if t < 10.0:
            env = 0.25 * (t / 3.0 if t < 3.0 else 1.0)
        elif t < 30.0:
            env = 0.35 + 0.1 * ((t - 10.0) / 20.0)
        elif t < 50.0:
            env = 0.30  # analytical section
        elif t < 62.0:
            env = 0.50  # climax tension
        else:
            env = 0.35  # post drop / ending
            
        samples[i] += drone * env
        
    # 2. Rhythmic Clock Tick & Pulse (Active from 8s onwards, intense from 15s-62s)
    tick_interval = beat_dur / 2.0  # 8th notes
    num_ticks = int(duration_sec / tick_interval)
    
    for tk in range(num_ticks):
        t_tick = tk * tick_interval
        if 62.0 <= t_tick <= 64.2:
            continue
        if t_tick < 8.0:
            continue
            
        start_idx = int(t_tick * sample_rate)
        # Alternate high/low tick
        f_tick = 3200.0 if (tk % 2 == 0) else 2400.0
        intensity = 0.18 if t_tick < 30.0 else (0.28 if t_tick < 50.0 else 0.35)
        
        tick_len = int(sample_rate * 0.04)
        for j in range(tick_len):
            idx = start_idx + j
            if idx >= total_samples:
                break
            t_rel = j / sample_rate
            env = math.exp(-t_rel * 90.0)
            samples[idx] += math.sin(2 * math.pi * f_tick * t_rel) * env * intensity
            
    # 3. Muted Kick Heartbeat Pulse on downbeats (12s to 62s)
    for b in range(total_beats):
        t_beat = b * beat_dur
        if t_beat < 12.0 or (62.0 <= t_beat <= 64.2):
            continue
            
        start_idx = int(t_beat * sample_rate)
        kick_len = int(sample_rate * 0.18)
        k_env_scale = 0.35 if t_beat < 30.0 else (0.45 if t_beat < 50.0 else 0.60)
        
        for j in range(kick_len):
            idx = start_idx + j
            if idx >= total_samples:
                break
            t_rel = j / sample_rate
            f_sweep = 90.0 * math.exp(-t_rel * 25.0) + 42.0
            k_env = math.exp(-t_rel * 14.0)
            samples[idx] += math.sin(2 * math.pi * f_sweep * t_rel) * k_env * k_env_scale

    # 4. Analytical Arpeggio (30s to 50s): D minor mysterious documentary synth
    arp_notes = [293.66, 349.23, 440.0, 523.25, 440.0, 349.23]  # D4, F4, A4, C5, A4, F4
    arp_step = beat_dur / 4.0  # 16th notes
    start_arp_t = 30.0
    end_arp_t = 50.0
    num_arp_steps = int((end_arp_t - start_arp_t) / arp_step)
    
    for s in range(num_arp_steps):
        t_note = start_arp_t + s * arp_step
        start_idx = int(t_note * sample_rate)
        note_f = arp_notes[s % len(arp_notes)]
        note_len = int(sample_rate * 0.15)
        
        for j in range(note_len):
            idx = start_idx + j
            if idx >= total_samples:
                break
            t_rel = j / sample_rate
            env = math.exp(-t_rel * 18.0)
            # Gentle filtered square/sine blend
            tone = 0.7 * math.sin(2 * math.pi * note_f * t_rel) + 0.3 * math.sin(2 * math.pi * (note_f * 2) * t_rel)
            samples[idx] += tone * env * 0.16

    # 5. Final Reveal Sting at 64.5s
    sting_start = int(64.5 * sample_rate)
    sting_len = int(sample_rate * 3.5)
    for j in range(sting_len):
        idx = sting_start + j
        if idx >= total_samples:
            break
        t_rel = j / sample_rate
        env = math.exp(-t_rel * 2.0)
        low_boom = math.sin(2 * math.pi * 55.0 * t_rel) * env * 0.7
        shimmer = math.sin(2 * math.pi * 880.0 * t_rel) * math.exp(-t_rel * 4.0) * 0.25
        samples[idx] += (low_boom + shimmer)

    # Master gentle compression & normalization to -18 dBFS peak
    max_val = max(abs(s) for s in samples) or 1.0
    normalized = [s / max_val * 0.72 for s in samples]
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(output_file), 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        raw_bytes = bytearray()
        for s in normalized:
            val = max(-1.0, min(1.0, s))
            int_val = int(val * 32767)
            raw_bytes.extend(struct.pack('<h', int_val))
        wf.writeframes(raw_bytes)
        
    print(f"Generated bespoke cinematic tension score: {output_file} ({duration_sec}s)")

if __name__ == "__main__":
    out_path = Path(__file__).parent.parent / "assets" / "bgm" / "cinematic_tension_score.wav"
    generate_cinematic_score(out_path, 75.0)
