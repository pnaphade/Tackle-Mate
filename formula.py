import reconstruct
import numpy as np
import matplotlib.pyplot as plt


def score(video_filepath):

    keypoints_timeseries = reconstruct.reconstruct(video_filepath)

    n_frames = len(keypoints_timeseries)
    print("Number of frames:", n_frames)

    '''

    # For the first framee: 6 people x 17 keypoints x (y coord, x coord, conf)
    print("Shape of keypoints at each frame:", keypoints_timeseries[0].shape)

    # Extract keypoints for first person
    person0 = np.array([person[0] for person in keypoints_timeseries])
    print("Shape of keypoints timeseries for person 0:", person0.shape) # frames, 17, 3
    print("-----------------------------------------------------------")


    body_keypoints = ["nose", "left eye", "right eye", "left ear",
            "right ear", "left shoulder", "right shoulder", "left elbow",
            "right elbow", "left wrist", "right wrist", "left hip", "right hip",
            "left knee", "right knee", "left ankle", "right ankle"]

    keypoints_index = np.arange(len(body_keypoints))
    body_index = dict(zip(body_keypoints, keypoints_index))

    # Final dimension of person array is encoded as y, x, confidence
    coords_index = {"y":0, "x":1, "conf":2}

    # Extract keypoints time series

    left_shoulder_y = person0[:, body_index["left shoulder"], coords_index["y"]]
    left_shoulder_y = 1 - left_shoulder_y   # transform so 1 is highest
    '''
    '''
    left_ankle_y = person0[:, body_index["left ankle"], coords_index["y"]]
    left_ankle_y = 1 - left_ankle_y   # transform so 1 is highest
    '''

    '''
    # TO DO take score mask so we only compare valid keypoints estimations
    score_lshoulder = person0[:, body_index["left shoulder"], coords_index["conf"]]
    score_lshoulder_mask = score_lshoulder > 0.1
    left_shoulder_y_scored = left_shoulder_y[score_lshoulder_mask]

    print("shape of left_shoulder_y:", left_shoulder_y.shape)
    print("shape of score_lshoulder_mask", score_lshoulder_mask.shape)
    print("number of frames with score > 0.1", score_lshoulder_mask.sum())
    print("shape of left_shoulder_y_scored", left_shoulder_y_scored.shape)
    print(left_shoulder_y_scored)

    fig1, ax1 = plt.subplots()
    ax1.plot(left_shoulder_y_scored)
    ax1.set_xlabel("Frames")
    ax1.set_ylabel("Left shoulder x position")

    plt.show()
    '''

    scores = {}
    scores["height"] = 0
    scores["accel"] = 0
    scores["wrap"] = 0

    print(scores)
    #return scores

    return n_frames


    '''
    # Take average of left ankle y position
    avg_left_ankle_y = np.mean(left_ankle_y)



    # Compute difference between shoulder and avg ankle height
    shoulder_avankle_diff = left_shoulder_y - avg_left_ankle_y

    should_start = shoulder_avankle_diff[0]
    should_min = np.min(shoulder_avankle_diff)
    print("Start should height:", round(should_start, 3))
    print("Minimum should height:", round(should_min, 3))
    should_percent_change = 100*(should_min-should_start)/(should_start)
    should_percent_change = abs(round(should_percent_change, 2))
    print("Percent change in shoulder height:", should_percent_change)




    code for calculating acceleration
    left_shoulder_x = person0[:, body_index["left shoulder"], coords_index["x"]]
    score0 = person0[:, body_index["left shoulder"], coords_index["conf"]]
    score_mask = score0 > 0.5
    print("Shape of score mask:", score_mask.shape)
    print("Number of frames with score > 0.5:", score_mask.sum())

    # don't include frames with a score less than 0.5
    left_shoulder_x = left_shoulder_x[score_mask]
    left_shoulder_x = 1 - left_shoulder_x   # transform so 1 is highest

    fig1, ax1 = plt.subplots()
    ax1.plot(left_shoulder_x)
    ax1.set_xlabel("Frames")
    ax1.set_ylabel("Left shoulder x position")

    plt.show()
    '''

'''
    # Scoring percent in shoulder height change
    if(should_percent_change < 20):
        score = 0
    if(20 <= should_percent_change  < 30):
        score = 1
    if(30 <= should_percent_change < 40):
        score = 2
    if(should_percent_change >= 40):
        score = 3

    feedback = {0:"poor", 1:"fair", 2:"good", 3:"excellent"}
    print("-----------------------------------------------------------")
    print(f"Tackle height score: {score}/3, {feedback[score]}")
    print("-----------------------------------------------------------")


    visualize(shoulder_avankle_diff)

    return {"start shoulder":should_start, "min shoulder":should_min, \
            "percent change":should_percent_change, "score":score, \
            "feedback":feedback[score]}
            '''


'''
def visualize(shoulder_avankle_diff):
    fig1, ax1 = plt.subplots()
    ax1.plot(shoulder_avankle_diff)
    ax1.set_xlabel("Frames")
    ax1.set_ylabel("Left shoulder y position - left ankle y position")
    ax1.set_title("Change in left shoulder height")

    #plt.show()
    plt.close('all')
'''

if __name__ == '__main__':
    score('videos/train/32_333.MOV')

# Using shoulder_ankle_diff or shoulder_avankle_diff, calculate the
# minimum and maximum diffs and then take the percent diff between them
# This represents the percent the tackler dropped their shoulders.
# Encode some range that matches percentages to scores.
# Deliver scores.
# relies on video being trimmed to isolate tackle
