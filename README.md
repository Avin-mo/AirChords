# AirChords 🎵

Play music chords in real time using hand gestures and computer vision.

## Demo

Show a chord with your right hand and a chord type with your left hand — AirChords detects both signs and plays the corresponding chord instantly. Hold the signs to sustain the chord. Make a fist with either hand to pause.

## How It Works

- Right hand controls the chord root (C, D, E, F, G, A, B)
- Left hand controls the chord type (Major, Minor, 7th, Maj7, Sus2, Sus4, Dim, Aug)
- Both hands together = 64 possible chords
- Fist = pause

## Tech Stack

- **MediaPipe** — real-time hand landmark detection (21 points per hand)
- **OpenCV** — webcam capture and UI rendering
- **NumPy** — sine wave generation for chord synthesis
- **SoundDevice** — real-time audio playback
- **Threading** — background audio playback without blocking the webcam loop
- **Python 3.11**

## What I Learned

### Computer Vision

- How MediaPipe represents a hand as 21 numbered landmarks with normalized (x, y, z) coordinates
- How to detect finger states by comparing fingertip and knuckle y-coordinates
- Why the thumb requires x-axis comparison instead of y-axis, and why left and right hands need opposite conditions
- How to correct for mirrored webcam output when drawing UI elements over landmarks
- How to detect which hand is which using `multi_handedness` alongside `multi_hand_landmarks`

### Audio & Signal Processing

- How sound is represented as a sine wave: $y = amplitude * sin(2π * frequency * t)$
- How a chord is built by summing multiple sine waves at different frequencies
- How musical intervals work — semitones and the formula freq \* 2^(semitones/12)$ to calculate note frequencies from a root
- How to apply a fade-in envelope to avoid abrupt audio starts
- How to loop audio indefinitely for chord sustain

### Software Engineering

- How to structure a Python project into modules (`src/ui.py`, `src/hand_tracker.py`, `src/audio.py`, `src/config.py`)
- How Python imports work across files and why `__init__.py` is needed
- How to use dictionaries instead of long if-statement chains for cleaner gesture-to-chord mapping
- How threading works and why it's needed to run audio and video simultaneously
- How to prevent audio retriggering every frame using a `last_chord` state variable
- Conventional commit messages and clean Git history

## Installation

```bash
pip install opencv-python mediapipe numpy sounddevice
```

## Run

```bash
python main.py
```

## Hand Signs

### Right Hand — Chord Root

| Sign                          | Chord |
| ----------------------------- | ----- |
| Open palm                     | C     |
| Thumb only                    | D     |
| Thumb + index                 | E     |
| Thumb + index + middle        | F     |
| Thumb + index + middle + ring | G     |
| Thumb + pinky                 | A     |
| Thumb + index + pinky         | B     |
| Fist                          | Pause |

### Left Hand — Chord Type

| Sign          | Type  |
| ------------- | ----- |
| Open palm     | Major |
| Peace         | Minor |
| OK sign       | 7th   |
| Rock          | Maj7  |
| Shaka         | Sus2  |
| Gun point     | Sus4  |
| Pinky up      | Dim   |
| Three fingers | Aug   |
| Fist          | Pause |

## Credits

Hand tracking built with [MediaPipe](https://mediapipe.dev) by Google.
