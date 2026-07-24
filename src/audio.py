import numpy as np
import sounddevice as sd
import threading


# y = amplitude * sin(2 * pi * frequency * t)
t = np.linspace(0, 2, 44100 * 2)

NOTE_FREQ = {
    "C":  261.63,
    "D":  293.66,
    "E":  329.63,
    "F":  349.23,
    "F#": 369.99,
    "G":  392.00,
    "A":  440.00,
    "B":  493.88,
}

CHORD_INTERVALS = {
    "Major": [0, 4, 7],
    "Minor": [0, 3, 7],
    "7th":   [0, 4, 7, 10],
    "Maj7":  [0, 4, 7, 11],
    "Sus2":  [0, 2, 7],
    "Sus4":  [0, 5, 7],
    "Dim":   [0, 3, 6],
    "Aug":   [0, 4, 8],
}

def generate_chord(root, chord_type):
    t = np.linspace(0, 2, 44100 * 2)
    root_freq = NOTE_FREQ.get(root)
    intervals = CHORD_INTERVALS.get(chord_type)
    wave = np.zeros(44100 * 2)
    for i in intervals:
        freq = root_freq * 2**(i/12)
        wave += np.sin(2 * np.pi * freq * t)
    
    # fade in over 0.1 seconds
    fade_samples = int(44100 * 0.3)
    wave[:fade_samples] *= np.linspace(0, 1, fade_samples)
    
    return wave

def play_chord(root, chord_type):
    wave = generate_chord(root, chord_type)
    thread = threading.Thread(target=lambda: sd.play(wave, samplerate=44100, loop=True))
    thread.start()
    
def stop_chord():
    sd.stop()
