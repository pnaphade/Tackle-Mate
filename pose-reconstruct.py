# Adapted from https://google.github.io/mediapipe/solutions/pose.html

from turtle import left
import cv2
import mediapipe as mp
import sys
import numpy as np
import matplotlib.pyplot as plt

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

FRAME_RATE = 30
fourcc = cv2.VideoWriter_fourcc('m', 'p', 'g', '4')
input_vid = sys.argv[1]
cap = cv2.VideoCapture(input_vid)

frame_counter = 0
landmarks_timeseries = []

with mp_pose.Pose(min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose: # how to tune these parameters?

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

# Make landmarks_timeseries body_areas x time
landmarks_timeseries = np.array(landmarks_timeseries).transpose()

print(landmarks_timeseries.shape)

left_should = landmarks_timeseries[body_index["left shoulder"]]

left_should_x = np.zeros_like(left_should)
left_should_y = np.zeros_like(left_should)
left_should_z = np.zeros_like(left_should)

# Unpacking x, y, z coords from each NormalizedLandmark object
for i in range(len(left_should)):
    left_should_x[i] = left_should[i].x
    left_should_y[i] = left_should[i].y
    left_should_z[i] = left_should[i].z


fig1, ax1 = plt.subplots()
ax1.plot(left_should_x)
ax1.set_xlabel("Frames")
ax1.set_ylabel("Normalized X position")

fig2, ax2 = plt.subplots()
ax2.plot(left_should_y)
ax2.set_xlabel("Frames")
ax2.set_ylabel("Normalized Y position")

fig3, ax3 = plt.subplots()
ax3.plot(left_should_z)
ax3.set_xlabel("Frames")
ax3.set_ylabel("Normalized Z position")

plt.show()
'''
plt.plot(left_should_x)
plt.show()

plt.plot(left_should_y)
plt.show()

plt.plot(left_should_z)
plt.show()
'''

'''
fig, ax = plt.subplots()
ax.plot(left_should_x)
fig.show()
'''

cap.release()
