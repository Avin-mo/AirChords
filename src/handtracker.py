import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


LEFT_HAND_CHORDS = {
    (False, False, False, False, False): "fist",
    (False, True, True, False, False):   "C",
    (True, True, True, True, True):      "D",
    (False, False, True, True, True):    "E",
    (True, True, False, False, True):    "F",
    (True, False, False, False, True):   "G",
    (True, True, True, False, False):    "A",
    (False, False, False, False, True):  "B",
    (False, True, True, True, False):    "F#",
}

RIGHT_HAND_TYPES = {
    (False, False, False, False, False): "fist",
    (True, True, True, True, True):     "Major",
    (False, True, True, False, False):  "Minor",
    (False, False, True, True, True):   "7th",
    (True, True, False, False, True):   "Maj7",
    (True, False, False, False, True):  "Sus2",
    (True, True, True, False, False):   "Sus4",
    (False, False, False, False, True): "Dim",
    (False, True, True, True, False):   "Aug",
}

def detect_chord(thumb, index, middle, ring, pinky):
    return LEFT_HAND_CHORDS.get((thumb, index, middle, ring, pinky))

def detect_sign(thumb, index, middle, ring, pinky):
    return RIGHT_HAND_TYPES.get((thumb, index, middle, ring, pinky))