# Adapted from https://google.github.io/mediapipe/solutions/pose.html

import cv2
import mediapipe as mp
import sys
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

FRAME_RATE = 30
fourcc = cv2.VideoWriter_fourcc('m', 'p', 'g', '4')
input_vid = sys.argv[1]
cap = cv2.VideoCapture(input_vid)

frame_counter = 0
landmarks_timeseries = []

with mp_pose.Pose(min_detection_confidence=0.1,
        min_tracking_confidence=0.1) as pose: # how to tune these parameters?

    while cap.isOpened():
        success, image = cap.read()

        if not success:
            print("Ignoring empty camera frame.")
            break

        frame_counter += 1

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        if (results.pose_landmarks is not None):
            landmarks_timeseries.append(results.pose_landmarks.landmark)

        # Draw the pose annotation on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

        # Display
        cv2.imshow('MediaPipe Pose', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break

print("Total number of frames:", frame_counter)
print("Total number of frames with landmarks calculated:",
        len(landmarks_timeseries))
landmarks_50 = landmarks_timeseries[50]
print("Number of landmarks:", len(landmarks_50))

body_areas = ["left shoulder", "right shoulder", "left elbow",
                    "right elbow", "left wrist", "right wrist",
                    "left hip", "right hip", "left knee", "right knee",
                    "left ankle", "right ankle"]
body_areas_index = [11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28]

body_index = dict(zip(body_areas, body_areas_index))

for body, index in body_index.items():
    print(body)
    print(landmarks_50[index])
    print()

cap.release()
