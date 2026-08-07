import numpy as np
import sounddevice as sd
import threading

SAMPLE_RATE = 44100

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


def generate_chord(root, chord_type):
    root_freq = NOTE_FREQ[root]
    intervals = CHORD_INTERVALS[chord_type]

    # snap length to whole cycles of the root so the loop point is seamless
    n_cycles = max(1, int(root_freq * 8))
    duration = n_cycles / root_freq
    n_samples = int(SAMPLE_RATE * duration)
    t = np.linspace(0, duration, n_samples, endpoint=False)

    weights = [1 / (n + 1) for n in range(len(intervals))]
    total_weight = sum(weights)

    wave = np.zeros(n_samples, dtype=np.float64)
    for n, i in enumerate(intervals):
        freq = root_freq * 2 ** (i / 12)
        wave += (weights[n] / total_weight) * np.sin(2 * np.pi * freq * t)

    return wave.astype(np.float32)


def preload_chords():
    for root in NOTE_FREQ:
        for chord_type in CHORD_INTERVALS:
            CHORD_CACHE[(root, chord_type)] = generate_chord(root, chord_type)
    _engine.start()


class _ChordEngine:
    """
    Keeps one continuous output stream open and handles chord changes
    by fading out, swapping the waveform, then fading in - instead of
    hard-cutting playback, which is what causes the pop.
    """

    FADE_SECONDS = 0.02  # 20ms fade, short enough to feel instant

    def __init__(self):
        self._lock = threading.Lock()
        self._stream = None

        self._state = "idle"  # idle | fading_out | fading_in | playing
        self._current_wave = None
        self._pending_wave = None
        self._pos = 0
        self._gain = 0.0
        self._fade_samples = int(SAMPLE_RATE * self.FADE_SECONDS)
        self._gain_step = 1.0 / self._fade_samples

    def start(self):
        if self._stream is None:
            self._stream = sd.OutputStream(
                channels=1,
                samplerate=SAMPLE_RATE,
                callback=self._callback,
                blocksize=0,
            )
            self._stream.start()

    def play(self, wave):
        with self._lock:
            if self._state == "idle":
                self._current_wave = wave
                self._pos = 0
                self._gain = 0.0
                self._state = "fading_in"
            else:
                self._pending_wave = wave
                self._state = "fading_out"

    def stop(self):
        with self._lock:
            if self._state in ("playing", "fading_in"):
                self._pending_wave = None
                self._state = "fading_out"

    def _read(self, wave, n):
        L = len(wave)
        idx = (self._pos + np.arange(n)) % L
        self._pos = (self._pos + n) % L
        return wave[idx]

    def _callback(self, outdata, frames, time_info, status):
        out = np.zeros(frames, dtype=np.float32)

        with self._lock:
            i = 0
            while i < frames:
                if self._state == "idle":
                    break

                elif self._state == "fading_out":
                    n = min(frames - i, self._fade_samples)
                    if self._current_wave is not None:
                        chunk = self._read(self._current_wave, n)
                        ramp = np.clip(self._gain - self._gain_step * np.arange(n), 0, 1)
                        out[i:i + n] += chunk * ramp
                        self._gain = max(self._gain - self._gain_step * n, 0.0)
                    else:
                        self._gain = 0.0

                    if self._gain <= 0.0:
                        self._current_wave = self._pending_wave
                        self._pending_wave = None
                        self._pos = 0
                        self._state = "fading_in" if self._current_wave is not None else "idle"
                    i += n

                elif self._state == "fading_in":
                    n = min(frames - i, self._fade_samples)
                    chunk = self._read(self._current_wave, n)
                    ramp = np.clip(self._gain + self._gain_step * np.arange(n), 0, 1)
                    out[i:i + n] += chunk * ramp
                    self._gain = min(self._gain + self._gain_step * n, 1.0)

                    if self._gain >= 1.0:
                        self._state = "playing"
                    i += n

                elif self._state == "playing":
                    n = frames - i
                    chunk = self._read(self._current_wave, n)
                    out[i:i + n] += chunk
                    i += n

        outdata[:, 0] = out


_engine = _ChordEngine()


def play_chord(root, chord_type):
    wave = CHORD_CACHE.get((root, chord_type))
    if wave is not None:
        _engine.play(wave)


def stop_chord():
    _engine.stop()