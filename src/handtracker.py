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

    
def detect_sign(thumb, index, middle, ring, pinky):
    if (thumb, index, middle, ring, pinky) == (False, False, False, False, False):
        return "fist"
    
    if (thumb, index, middle, ring, pinky) == (True, True, True, True, True):
        return "open palm"
    
    if (thumb, index, middle, ring, pinky) == (False, True, True, False, False):
        return "peace"
    
    if (thumb, index, middle, ring, pinky) == (False, False, True, True, True):
        return "ok"
    
    if (thumb, index, middle, ring, pinky) == (True, True, False, False, True):
        return "rock"
    
    if (thumb, index, middle, ring, pinky) == (True, False, False, False, True):
        return "shaka"
    
    if (thumb, index, middle, ring, pinky) == (True, True, True, False, False):
        return "gun point"
    
    if (thumb, index, middle, ring, pinky) == (False, False, False, False, True):
        return "pinky"