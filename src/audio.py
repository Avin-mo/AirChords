import numpy as np
import sounddevice as sd
import threading
import time

current_stream = None

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

CHORD_CACHE = {}

def preload_chords():
    for root in NOTE_FREQ:
        for chord_type in CHORD_INTERVALS:
            CHORD_CACHE[(root, chord_type)] = generate_chord(root, chord_type)


def generate_chord(root, chord_type):
    t = np.linspace(0, 8, 44100 * 8, endpoint=False)
    root_freq = NOTE_FREQ.get(root)
    intervals = CHORD_INTERVALS.get(chord_type)
    wave = np.zeros(44100 * 8)
    for n, i in enumerate(intervals):
        freq = root_freq * 2**(i/12)
        amp = 1 / (n + 1)**1.5  # each higher note in the chord a bit quieter
        wave += amp * np.sin(2 * np.pi * freq * t)
    wave /= np.sum([1/(n+1) for n in range(len(intervals))])  # normalize to avoid clipping

    fade_samples = int(44100 * 0.1)
    wave[:fade_samples] *= np.linspace(0, 1, fade_samples)
    wave[-fade_samples:] *= np.linspace(1, 0, fade_samples)  # fade out too
    return wave

def play_chord(root, chord_type):
    global current_stream
    wave = CHORD_CACHE.get((root, chord_type))
    if wave is None:
        return
    def _play():
        sd.play(wave, samplerate=44100, loop=True)
    thread = threading.Thread(target=_play)
    thread.start()
    
def stop_chord(fade_ms=30):
    sd.stop()
