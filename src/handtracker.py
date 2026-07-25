import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


def get_finger_states(hand_landmarks, label):

    index_up = hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y
    middle_up = hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y
    ring_up = hand_landmarks.landmark[16].y < hand_landmarks.landmark[14].y
    pinky_up = hand_landmarks.landmark[20].y < hand_landmarks.landmark[18].y

    if label == "Left":
        thumb_up = hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x
    else:
        thumb_up = hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x

    return thumb_up, index_up, middle_up, ring_up, pinky_up

    
RIGHT_HAND_CHORDS = {
    (False, False, False, False, False): "pause",
    (True, True, True, True, True):   "G",
    (True, False, False, False, False):  "C",
    (True, True, False, False, False):    "D",
    (True, True, True, False, False):    "E",
    (True, True, True, True, False):   "F",
    (True, False, False, False, True):    "A",
    (True, True, False, False, True):  "B"
}

LEFT_HAND_TYPES = {
    (False, False, False, False, False): "pause",
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
    return RIGHT_HAND_CHORDS.get((thumb, index, middle, ring, pinky))

def detect_sign(thumb, index, middle, ring, pinky):
    return LEFT_HAND_TYPES.get((thumb, index, middle, ring, pinky))