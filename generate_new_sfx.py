import numpy as np
import os
import struct
import random

SFX_DIR = "sfx"
SAMPLE_RATE = 22050

def write_wav(filename, data, sample_rate=SAMPLE_RATE):
    data = np.clip(data, -1.0, 1.0)
    int_data = (data * 32767).astype(np.int16)
    filepath = os.path.join(SFX_DIR, filename)
    n_samples = len(int_data)
    with open(filepath, 'wb') as f:
        f.write(b'RIFF')
        data_size = n_samples * 2
        f.write(struct.pack('<I', 36 + data_size))
        f.write(b'WAVE')
        f.write(b'fmt ')
        f.write(struct.pack('<I', 16))
        f.write(struct.pack('<H', 1))
        f.write(struct.pack('<H', 1))
        f.write(struct.pack('<I', sample_rate))
        f.write(struct.pack('<I', sample_rate * 2))
        f.write(struct.pack('<H', 2))
        f.write(struct.pack('<H', 16))
        f.write(b'data')
        f.write(struct.pack('<I', data_size))
        f.write(int_data.tobytes())
    print(f"Generated: {filename}")

def fade_in_out(data, fade_in=0.1, fade_out=0.3):
    n = len(data)
    fi = int(fade_in * SAMPLE_RATE)
    fo = int(fade_out * SAMPLE_RATE)
    if fi > 0 and len(data) > fi:
        data[:fi] *= np.linspace(0, 1, fi)
    if fo > 0 and len(data) > fo:
        data[-fo:] *= np.linspace(1, 0, fo)
    return data

def generate_magic_chime():
    duration = 2.0
    t = np.linspace(0, duration, int(duration * SAMPLE_RATE), endpoint=False)
    freqs = [880, 1108.73, 1318.51, 1760, 2217.46]  # A major pentatonic
    signal = np.zeros_like(t)
    for i, f in enumerate(freqs):
        delay = i * 0.05
        delay_idx = int(delay * SAMPLE_RATE)
        t_sub = t[:len(t)-delay_idx]
        env = np.exp(-3 * t_sub)
        wave = np.sin(2 * np.pi * f * t_sub) * env * 0.2
        signal[delay_idx:] += wave
    return fade_in_out(signal, 0.01, 0.5)

def generate_cyber_whoosh():
    duration = 1.2
    t = np.linspace(0, duration, int(duration * SAMPLE_RATE), endpoint=False)
    noise = np.random.normal(0, 0.5, len(t))
    freq = np.linspace(800, 200, len(t))
    env = np.sin(np.pi * (t / duration)) ** 2
    # Simple FM synthesis for cyber feel
    mod = np.sin(2 * np.pi * freq * t) * noise
    return fade_in_out(mod * env * 0.4, 0.1, 0.3)

def generate_retro_ui_click():
    duration = 0.15
    t = np.linspace(0, duration, int(duration * SAMPLE_RATE), endpoint=False)
    freq1 = np.linspace(1200, 800, len(t))
    freq2 = np.linspace(2400, 1200, len(t))
    signal = np.sin(2 * np.pi * freq1 * t) * 0.3 + np.sin(2 * np.pi * freq2 * t) * 0.2
    # Add a bit of square wave crunch
    signal = np.sign(signal) * np.abs(signal)**0.5
    env = np.exp(-25 * t)
    return fade_in_out(signal * env, 0.01, 0.05)

if __name__ == "__main__":
    os.makedirs(SFX_DIR, exist_ok=True)
    for i in range(1, 4):
        write_wav(f"magic_chime_{i}.wav", generate_magic_chime() * random.uniform(0.8, 1.2))
        write_wav(f"cyber_whoosh_{i}.wav", generate_cyber_whoosh() * random.uniform(0.8, 1.2))
        write_wav(f"retro_ui_click_{i}.wav", generate_retro_ui_click() * random.uniform(0.8, 1.2))
