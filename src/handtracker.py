# Part of the code in this page (the main tracking functions) is from: https://colab.research.google.com/github/googlesamples/mediapipe/blob/main/examples/hand_landmarker/python/hand_landmarker.ipynb

import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    max_num_hands=3,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    

    # Draw the hand annotations on the image.
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

            index_up = hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y
            middle_up = hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y
            ring_up = hand_landmarks.landmark[16].y < hand_landmarks.landmark[14].y
            pinky_up = hand_landmarks.landmark[20].y < hand_landmarks.landmark[18].y

            if label == "Left":
                thumb_up = hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x
            else:
                thumb_up = hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x

            print(label, thumb_up, index_up, middle_up, ring_up, pinky_up)
            
        
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()