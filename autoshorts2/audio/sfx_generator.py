"""Procedural SFX Synthesizer for AutoShorts 2.0
Generates high-definition audio cues: coin clinks, cash rustle, tension pulse, digital scan, stamp impact.
"""

import math
import wave
import struct
import random
from pathlib import Path

def write_wav(filepath: Path, samples: list[float], sample_rate: int = 44100):
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(filepath), 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        # Convert floats in [-1.0, 1.0] to int16
        raw_bytes = bytearray()
        for s in samples:
            val = max(-1.0, min(1.0, s))
            int_val = int(val * 32767)
            raw_bytes.extend(struct.pack('<h', int_val))
        wf.writeframes(raw_bytes)

def generate_coins_sfx(filepath: Path, sample_rate: int = 44100):
    """Multiple metallic coin clinks with high frequency ringing and resonance."""
    duration = 1.2
    total_samples = int(sample_rate * duration)
    samples = [0.0] * total_samples
    
    # 5 distinct metallic coin impacts
    impact_times = [0.0, 0.08, 0.22, 0.35, 0.52]
    coin_freqs = [2400, 3100, 4200, 5800, 7100]
    
    for t_hit in impact_times:
        start_idx = int(t_hit * sample_rate)
        freq = random.choice(coin_freqs) * random.uniform(0.95, 1.05)
        for i in range(start_idx, total_samples):
            t = (i - start_idx) / sample_rate
            # High-Q decaying metallic sine
            envelope = math.exp(-t * 28.0)
            if envelope < 0.001:
                break
            ring1 = math.sin(2 * math.pi * freq * t)
            ring2 = 0.5 * math.sin(2 * math.pi * (freq * 1.48) * t)
            ring3 = 0.25 * math.sin(2 * math.pi * (freq * 2.15) * t)
            # Transient click
            click = (1.0 if t < 0.003 else 0.0) * (random.uniform(-1, 1))
            samples[i] += (ring1 + ring2 + ring3 + click * 0.8) * envelope * 0.45
            
    # Normalize
    max_val = max(abs(s) for s in samples) or 1.0
    samples = [s / max_val * 0.85 for s in samples]
    write_wav(filepath, samples, sample_rate)

def generate_tension_pulse_sfx(filepath: Path, sample_rate: int = 44100):
    """Deep cinematic sub-bass tension pulse (60Hz -> 38Hz) with dark overtone."""
    duration = 2.0
    total_samples = int(sample_rate * duration)
    samples = [0.0] * total_samples
    
    for i in range(total_samples):
        t = i / sample_rate
        # Pitch envelope sweeps down from 75Hz to 38Hz
        freq = 75.0 * math.exp(-t * 1.5) + 38.0
        env = math.exp(-t * 2.2)
        # Sub sine + subtle distortion
        sub = math.sin(2 * math.pi * freq * t)
        distorted = math.tanh(sub * 2.0) * 0.5 + sub * 0.5
        samples[i] = distorted * env * 0.95
        
    write_wav(filepath, samples, sample_rate)

def generate_cash_count_sfx(filepath: Path, sample_rate: int = 44100):
    """Crisp high-speed paper cash bills flicking."""
    duration = 0.9
    total_samples = int(sample_rate * duration)
    samples = [0.0] * total_samples
    
    # 6 rapid paper bill snaps
    bill_times = [0.02, 0.12, 0.22, 0.31, 0.41, 0.50, 0.61]
    for b_t in bill_times:
        start_idx = int(b_t * sample_rate)
        for i in range(start_idx, min(start_idx + int(sample_rate * 0.08), total_samples)):
            t = (i - start_idx) / sample_rate
            env = math.exp(-t * 85.0)
            noise = (random.random() * 2.0 - 1.0)
            thump = math.sin(2 * math.pi * 320 * t) * 0.4
            samples[i] += (noise * 0.7 + thump) * env * 0.6
            
    max_val = max(abs(s) for s in samples) or 1.0
    samples = [s / max_val * 0.8 for s in samples]
    write_wav(filepath, samples, sample_rate)

def generate_digital_scan_sfx(filepath: Path, sample_rate: int = 44100):
    """High-tech digital HUD confirmation chirps."""
    duration = 0.5
    total_samples = int(sample_rate * duration)
    samples = [0.0] * total_samples
    
    chirp_times = [0.0, 0.1]
    freqs = [880.0, 1760.0]
    for ct, f in zip(chirp_times, freqs):
        start_idx = int(ct * sample_rate)
        for i in range(start_idx, min(start_idx + int(sample_rate * 0.12), total_samples)):
            t = (i - start_idx) / sample_rate
            env = math.sin(math.pi * (t / 0.12))
            samples[i] += math.sin(2 * math.pi * f * t) * env * 0.45
            
    write_wav(filepath, samples, sample_rate)

def generate_stamp_impact_sfx(filepath: Path, sample_rate: int = 44100):
    """Heavy official stamp / gavel slam impact."""
    duration = 1.0
    total_samples = int(sample_rate * duration)
    samples = [0.0] * total_samples
    
    for i in range(total_samples):
        t = i / sample_rate
        env = math.exp(-t * 9.0)
        click_env = math.exp(-t * 120.0)
        low_thud = math.sin(2 * math.pi * 65.0 * t) * env
        wood_crack = (random.random() * 2.0 - 1.0) * click_env * 0.8
        mid_body = math.sin(2 * math.pi * 180.0 * t) * math.exp(-t * 22.0) * 0.5
        samples[i] = (low_thud + wood_crack + mid_body) * 0.9
        
    max_val = max(abs(s) for s in samples) or 1.0
    samples = [s / max_val * 0.9 for s in samples]
    write_wav(filepath, samples, sample_rate)

def generate_all_sfx(sfx_dir: Path):
    sfx_dir.mkdir(parents=True, exist_ok=True)
    generate_coins_sfx(sfx_dir / "coins.wav")
    generate_tension_pulse_sfx(sfx_dir / "tension_pulse.wav")
    generate_cash_count_sfx(sfx_dir / "cash_count.wav")
    generate_digital_scan_sfx(sfx_dir / "digital_scan.wav")
    generate_stamp_impact_sfx(sfx_dir / "stamp_impact.wav")
    print(f"Generated 5 custom cinematic sound effects in {sfx_dir}")

if __name__ == "__main__":
    generate_all_sfx(Path(__file__).parent.parent / "assets" / "sfx")
