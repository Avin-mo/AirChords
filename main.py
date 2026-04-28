import cv2
from src.ui import draw_circles

def main():
    cap = cv2.VideoCapture(0)
    width = int(cap.get(3))
    height = int(cap.get(4))


    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)
        
        frame = draw_circles(frame, width, height)

        cv2.imshow('AIRCHORDS', frame)
        
        if cv2.waitKey(1) == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()