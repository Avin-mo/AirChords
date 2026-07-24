import cv2
import mediapipe as mp
from src.handtracker import detect_chord, detect_sign, get_finger_states
from src.ui import draw_hand_ui

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

def main():
    cap = cv2.VideoCapture(0)
    width = int(cap.get(3))
    height = int(cap.get(4))

    with mp_hands.Hands(
        model_complexity=0,
        max_num_hands=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:

        while cap.isOpened():
            success, image = cap.read()
            if not success:
                continue
            signs = {}

            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.multi_hand_landmarks:
                for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())

                    label = handedness.classification[0].label
                    label = "Left" if label == "Right" else "Right"

                    thumb, index, middle, ring, pinky = get_finger_states(hand_landmarks, label)

                    if label == "Left":
                        result = detect_chord(thumb, index, middle, ring, pinky)
                    else:
                        result = detect_sign(thumb, index, middle, ring, pinky)

                    signs[label] = (hand_landmarks, result)

            image = cv2.flip(image, 1)

            for label, (hand_landmarks, result) in signs.items():
                draw_hand_ui(image, hand_landmarks, result, width, height)

            chord = signs.get("Left", (None, None))[1]
            chord_type = signs.get("Right", (None, None))[1]

            if chord and chord_type and chord != "fist" and chord_type != "fist":
                print(f"{chord} {chord_type}")

            cv2.imshow('AirChords', image)
            if cv2.waitKey(1) == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()