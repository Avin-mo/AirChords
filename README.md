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

## Audio Quality Improvements

The chord synthesis in `audio.py` went through a few rounds of tuning to move from raw sine waves to something more pleasant to listen to during extended play.

### Harmonic amplitude tapering

Originally, each note in a chord was summed at full amplitude. Stacking multiple full-strength sine waves can clip and produces a buzzy, harsh tone. Each additional note is now weighted progressively lower and the total is normalized, which mimics how overtones decay in amplitude on real instruments and results in a warmer sound.

### Seamless loop boundaries

Chords are looped with `sd.play(..., loop=True)`, which jumps directly from the last sample back to the first. If the waveform isn't aligned at that boundary, it creates a discontinuity that's audible as a click on every loop. The buffer length is now sized to a whole number of cycles of the root frequency, so the waveform starts and ends at matching points and loops without popping.

### Softer harmonic falloff

A single sine wave is already about as soft as a waveform gets, so most of the earlier harshness came from equal-strength harmonics rather than the sine itself. Rolling off the higher intervals more steeply shifts the overall timbre from bright and edgy toward mellow and rounded.

### Fade-in and fade-out envelopes

Each cached chord waveform now fades in and out over a short window instead of starting and stopping abruptly. This avoids sharp amplitude jumps at the beginning and end of playback, which otherwise sound like clicks.

### Known limitation: stop-transition pops

`sd.stop()` cuts playback instantly, which usually isn't at a zero-crossing in the waveform, so switching chords can still produce a small pop. The fade-out on cached waveforms helps but doesn't fully solve this, since the interruption can happen mid-fade. A complete fix would require switching from `sd.play` to `sd.OutputStream`, which allows the amplitude to be ramped down live at the exact moment of interruption. This is a planned follow-up.

### Click-free chord transitions

Earlier versions spawned a new playback thread via `sd.play()` for each chord and used `sd.stop()` to cut the previous one off. Since `sd.stop()` interrupts playback at whatever amplitude the waveform happens to be at, this produced an audible pop on nearly every chord change.

Audio playback now runs through a single, persistent `sd.OutputStream` that stays open for the life of the program, rather than starting and stopping a stream per chord. Chord changes are handled by a small state machine (`idle`, `fading_out`, `fading_in`, `playing`) running inside the stream's callback: switching chords fades the current waveform's volume down to zero over ~20ms, swaps in the new waveform, then fades it back up. Because the transition always passes through silence smoothly instead of cutting mid-waveform, there's no click or pop.

Looping is also handled differently: instead of relying on `sd.play`'s built-in `loop=True` (which just restarts the buffer from index 0 with no awareness of waveform phase), a running sample position wraps around the buffer using modulo indexing. Combined with buffers already sized to whole cycles of the root frequency, this keeps looping seamless.

The public interface (`preload_chords()`, `play_chord()`, `stop_chord()`) is unchanged, so this was a drop-in replacement with no changes needed elsewhere in the codebase.

## Credits

Hand tracking built with [MediaPipe](https://mediapipe.dev) by Google.
