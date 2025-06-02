import cv2
import numpy as np

def create_test_video():
    width, height = 640, 480
    fps = 30
    duration = 10  # seconds

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('test_video.mp4', fourcc, fps, (width, height))

    for i in range(fps * duration):
        frame = np.zeros((height, width, 3), dtype=np.uint8)

        x1 = int(width/2 + 100 * np.sin(i/10))
        y1 = int(height/2 + 100 * np.cos(i/10))
        x2 = int(width/2 + 100 * np.sin(i/10 + np.pi))
        y2 = int(height/2 + 100 * np.cos(i/10 + np.pi))

        cv2.circle(frame, (x1, y1), 30, (0, 255, 0), -1)  # Green circle
        cv2.circle(frame, (x2, y2), 30, (0, 0, 255), -1)  # Red circle

        out.write(frame)

    out.release()
    print("Test video created successfully.")

if __name__ == '__main__':
    create_test_video()
