### extracts frames from video ###

#!/usr/bin/python3

import cv2
import os

video_path = './safari.mp4'
output_folder = 'frames'

cap = cv2.VideoCapture(video_path)
frame_count = 0

while True:
    ret, frame = cap.read()

    if not ret:
        break;

    frame_filename = os.path.join(output_folder, f'{frame_count:03d}.jpg')
    cv2.imwrite(frame_filename, frame)

    frame_count += 1

cap.release()
