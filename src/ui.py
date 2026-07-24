import cv2

def draw_hand_ui(image, hand_landmarks, sign, width, height):
    x_coords = [lm.x * width for lm in hand_landmarks.landmark]
    y_coords = [lm.y * height for lm in hand_landmarks.landmark]

    x_min, x_max = int(min(x_coords)), int(max(x_coords))
    y_min, y_max = int(min(y_coords)), int(max(y_coords))

    # mirror x to match flipped image
    flipped_x_min = width - x_max
    flipped_x_max = width - x_min

    padding = 20
    cv2.rectangle(image,
                  (flipped_x_min - padding, y_min - padding),
                  (flipped_x_max + padding, y_max + padding),
                  (255, 255, 255), 2)

    if sign:
        cv2.putText(image, sign,
                    (flipped_x_min - padding, y_min - padding - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)