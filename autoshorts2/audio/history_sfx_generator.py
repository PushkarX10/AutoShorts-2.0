"""Procedural Historical SFX Synthesizer
Generates historically appropriate audio cues:
- Bronze war horn (carnyx / Roman cornu blast)
- Armored legionary marching
- Pickaxe & timber fortification construction
- Bronze/iron shield & gladius clash
"""

import math
import struct
import wave
import random
from pathlib import Path

def write_wav(filepath: Path, samples: list[float], sample_rate: int = 44100):
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(filepath), 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        raw_bytes = bytearray()
        for s in samples:
            val = max(-1.0, min(1.0, s))
            int_val = int(val * 32767)
            raw_bytes.extend(struct.pack('<h', int_val))
        wf.writeframes(raw_bytes)

def generate_war_horn_sfx(filepath: Path, sample_rate: int = 44100):
    """Deep, menacing ancient bronze war horn blast (D3, 146.8Hz) with brassy overtones."""
    duration = 2.5
    total_samples = int(sample_rate * duration)
    samples = [0.0] * total_samples
    f0 = 146.83  # D3
    
    for i in range(total_samples):
        t = i / sample_rate
        # Envelope: swell then slow decay
        if t < 0.4:
            env = (t / 0.4) ** 1.5
        else:
            env = math.exp(-(t - 0.4) * 1.2)
            
        # Subtle pitch wobble / breath jitter
        jitter = 1.0 + 0.008 * math.sin(2 * math.pi * 5.5 * t)
        freq = f0 * jitter
        
        # Rich brass harmonics
        h1 = math.sin(2 * math.pi * freq * t)
        h2 = 0.7 * math.sin(2 * math.pi * (freq * 2) * t)
        h3 = 0.5 * math.sin(2 * math.pi * (freq * 3) * t)
        h4 = 0.35 * math.sin(2 * math.pi * (freq * 4) * t)
        h5 = 0.2 * math.sin(2 * math.pi * (freq * 5) * t)
        
        # Subtle brass distortion
        raw = (h1 + h2 + h3 + h4 + h5) * env
        samples[i] = math.tanh(raw * 1.8) * 0.85
        
    write_wav(filepath, samples, sample_rate)

def generate_marching_sfx(filepath: Path, sample_rate: int = 44100):
    """Rhythmic marching of heavy sandaled legionaries on dirt and gravel."""
    duration = 2.2
    total_samples = int(sample_rate * duration)
    samples = [0.0] * total_samples
    
    step_interval = 0.52
    num_steps = int(duration / step_interval)
    
    for s in range(num_steps):
        t_step = s * step_interval
        start_idx = int(t_step * sample_rate)
        step_len = int(sample_rate * 0.2)
        
        for j in range(step_len):
            idx = start_idx + j
            if idx >= total_samples:
                break
            t_rel = j / sample_rate
            env = math.exp(-t_rel * 25.0)
            low_thud = math.sin(2 * math.pi * 65.0 * t_rel) * env * 0.5
            gravel = (random.random() * 2.0 - 1.0) * math.exp(-t_rel * 45.0) * 0.35
            samples[idx] += (low_thud + gravel) * 0.8
            
    max_val = max(abs(s) for s in samples) or 1.0
    samples = [s / max_val * 0.8 for s in samples]
    write_wav(filepath, samples, sample_rate)

def generate_digging_sfx(filepath: Path, sample_rate: int = 44100):
    """Iron pickaxe striking hard earth and shoveling trenches."""
    duration = 1.6
    total_samples = int(sample_rate * duration)
    samples = [0.0] * total_samples
    
    hit_times = [0.05, 0.75]
    for ht in hit_times:
        start_idx = int(ht * sample_rate)
        for j in range(int(sample_rate * 0.45)):
            idx = start_idx + j
            if idx >= total_samples:
                break
            t_rel = j / sample_rate
            # Sharp metallic pick strike (1200Hz) decaying into gravel scrape
            strike = math.sin(2 * math.pi * 1200.0 * t_rel) * math.exp(-t_rel * 80.0) * 0.6
            scrape = (random.random() * 2.0 - 1.0) * math.exp(-t_rel * 14.0) * 0.4
            samples[idx] += (strike + scrape) * 0.75
            
    max_val = max(abs(s) for s in samples) or 1.0
    samples = [s / max_val * 0.85 for s in samples]
    write_wav(filepath, samples, sample_rate)

def generate_sword_clash_sfx(filepath: Path, sample_rate: int = 44100):
    """Heavy iron blade striking a bronze rimmed wooden shield."""
    duration = 1.4
    total_samples = int(sample_rate * duration)
    samples = [0.0] * total_samples
    
    for i in range(total_samples):
        t = i / sample_rate
        env = math.exp(-t * 12.0)
        ring_env = math.exp(-t * 22.0)
        
        wood_thump = math.sin(2 * math.pi * 95.0 * t) * env * 0.6
        metal_ring1 = math.sin(2 * math.pi * 2850.0 * t) * ring_env * 0.45
        metal_ring2 = math.sin(2 * math.pi * 4400.0 * t) * ring_env * 0.25
        scrape = (random.random() * 2.0 - 1.0) * math.exp(-t * 90.0) * 0.5
        
        samples[i] = (wood_thump + metal_ring1 + metal_ring2 + scrape) * 0.8
        
    max_val = max(abs(s) for s in samples) or 1.0
    samples = [s / max_val * 0.85 for s in samples]
    write_wav(filepath, samples, sample_rate)

def generate_all_history_sfx(target_dir: Path):
    target_dir.mkdir(parents=True, exist_ok=True)
    generate_war_horn_sfx(target_dir / "horn.wav")
    generate_marching_sfx(target_dir / "march.wav")
    generate_digging_sfx(target_dir / "digging.wav")
    generate_sword_clash_sfx(target_dir / "clash.wav")
    print(f"Generated 4 historical sound effects in {target_dir}")

if __name__ == "__main__":
    generate_all_history_sfx(Path(__file__).resolve().parent.parent.parent / "autoshorts2" / "assets" / "sfx")
