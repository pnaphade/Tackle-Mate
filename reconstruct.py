import os
import tensorflow as tf
import cv2
import numpy as np

# suppress all tensorflow info messages
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'


# Function to loop through each person detected and render
def loop_through_people(frame, keypoints_with_scores, edges, confidence_threshold):
    for person in keypoints_with_scores:
        draw_connections(frame, person, edges, confidence_threshold)
        draw_keypoints(frame, person, confidence_threshold)


def draw_keypoints(frame, keypoints, confidence_threshold):
    y, x, c = frame.shape
    shaped = np.squeeze(np.multiply(keypoints, [y,x,1]))

    for kp in shaped:
        ky, kx, kp_conf = kp
        if kp_conf > confidence_threshold:
            cv2.circle(frame, (int(kx), int(ky)), 6, (0,255,0), -1)


def draw_connections(frame, keypoints, edges, confidence_threshold):
    y, x, c = frame.shape
    shaped = np.squeeze(np.multiply(keypoints, [y,x,1]))

    for edge, color in edges.items():
        p1, p2 = edge
        y1, x1, c1 = shaped[p1]
        y2, x2, c2 = shaped[p2]

        if (c1 > confidence_threshold) & (c2 > confidence_threshold):
            cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0,0,255), 4)


def reconstruct(model, video_filepath):

    EDGES = {
    (0, 1): 'm',
    (0, 2): 'c',
    (1, 3): 'm',
    (2, 4): 'c',
    (0, 5): 'm',
    (0, 6): 'c',
    (5, 7): 'm',
    (7, 9): 'm',
    (6, 8): 'c',
    (8, 10): 'c',
    (5, 6): 'y',
    (5, 11): 'm',
    (6, 12): 'c',
    (11, 12): 'y',
    (11, 13): 'm',
    (13, 15): 'm',
    (12, 14): 'c',
    (14, 16): 'c'
    }

    print("-----------------------------------------------------------")
    print("Reading video from file", video_filepath)
    print("-----------------------------------------------------------")

    keypoints_timeseries = []
    cap = cv2.VideoCapture(video_filepath)
    fps = cap.get(cv2.CAP_PROP_FPS)

    while cap.isOpened():
        ret, frame = cap.read()

        if frame is None:
            break

        # Resize frame dims to multiple of 32 and longer side 256
        img = frame.copy()
        img = tf.image.resize_with_pad(tf.expand_dims(img, axis=0), 160,256)

        #img = tf.image.resize_with_pad(tf.expand_dims(img, axis=0), 128,256)
        input_img = tf.cast(img, dtype=tf.int32)

        # Feed frame to movenet
        results = model(input_img)

        # 6 people, 17 keypoints, and  y coord, x coord, confidence for each keypoint
        keypoints_with_scores = results['output_0'].numpy()[:,:,:51].reshape((6,17,3))
        keypoints_timeseries.append(keypoints_with_scores)

        # Draw body keypoints and edges for each person, confidence threshold
        loop_through_people(frame, keypoints_with_scores, EDGES, 0.3)

        #cv2.imshow('Movenet Multipose', frame)
        if cv2.waitKey(10) & 0xFF==ord('q'):
            break


    cap.release()
    cv2.destroyAllWindows()

    return keypoints_timeseries, fps
