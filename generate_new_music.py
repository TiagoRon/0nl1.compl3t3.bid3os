import numpy as np
import os
import struct

MUSIC_DIR = "music"
SAMPLE_RATE = 22050

def write_wav(filename, data, sample_rate=SAMPLE_RATE):
    data = np.clip(data, -1.0, 1.0)
    int_data = (data * 32767).astype(np.int16)
    filepath = os.path.join(MUSIC_DIR, filename)
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
    print(f"Generated Music: {filename}")

def generate_lofi_loop(duration=16.0):
    t = np.linspace(0, duration, int(duration * SAMPLE_RATE), endpoint=False)
    # Lofi vinyl crackle
    crackle = np.random.normal(0, 0.05, len(t))
    # Add sparse pops
    pops = np.zeros(len(t))
    for _ in range(int(duration * 2)):
        idx = np.random.randint(0, len(t))
        pops[idx] = np.random.normal(0, 0.5)
    
    # Warm electric piano chords (Cmaj7, Am7, Dm7, G7)
    bpm = 80
    beat_dur = 60 / bpm
    chord_dur = beat_dur * 4
    
    chords = [
        [261.63, 329.63, 392.00, 493.88], # Cmaj7
        [220.00, 261.63, 329.63, 392.00], # Am7
        [293.66, 349.23, 440.00, 523.25], # Dm7
        [196.00, 246.94, 293.66, 349.23], # G7
    ]
    
    music = np.zeros(len(t))
    for i, chord in enumerate(chords * 2): # loop twice
        start_idx = int(i * chord_dur * SAMPLE_RATE)
        end_idx = int((i + 1) * chord_dur * SAMPLE_RATE)
        if start_idx >= len(t): break
        if end_idx > len(t): end_idx = len(t)
        
        t_chord = t[:end_idx-start_idx]
        env = np.exp(-1.0 * t_chord) # decay
        
        for freq in chord:
            # simple sine + triangle for warm rhodes sound
            wave = (np.sin(2 * np.pi * freq * t_chord) * 0.7 + np.arcsin(np.sin(2 * np.pi * freq * t_chord)) * 0.3)
            music[start_idx:end_idx] += wave * env * 0.15
            
    # Simple low-pass filter
    kernel_size = 50
    kernel = np.ones(kernel_size) / kernel_size
    music_filtered = np.convolve(music, kernel, mode='same')
    
    final = crackle + pops + music_filtered
    return final

def generate_cyberpunk_loop(duration=16.0):
    t = np.linspace(0, duration, int(duration * SAMPLE_RATE), endpoint=False)
    bpm = 110
    beat_dur = 60 / bpm
    
    # Driving bassline (E minor)
    bass = np.zeros(len(t))
    notes = [82.41, 82.41, 98.00, 82.41, 110.00, 82.41, 98.00, 73.42] # E2, E2, G2, E2, A2, E2, G2, D2
    
    for i in range(int(duration / (beat_dur / 2))):
        start_idx = int(i * (beat_dur / 2) * SAMPLE_RATE)
        end_idx = int((i + 1) * (beat_dur / 2) * SAMPLE_RATE)
        if end_idx > len(t): break
        
        note = notes[i % len(notes)]
        t_note = t[:end_idx-start_idx]
        # Sawtooth wave
        wave = 2 * (t_note * note - np.floor(0.5 + t_note * note))
        env = np.exp(-5.0 * t_note)
        bass[start_idx:end_idx] += wave * env * 0.3
        
    return bass

if __name__ == "__main__":
    os.makedirs(MUSIC_DIR, exist_ok=True)
    write_wav("lofi_chill.wav", generate_lofi_loop())
    write_wav("cyberpunk_synth.wav", generate_cyberpunk_loop())
