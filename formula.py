import reconstruct

video= "test1.mov"
keypoints_timeseries = reconstruct.reconstruct(video_filepath=video)
print("Length of timeseries:", len(keypoints_timeseries))

# For the first framee: 6 people x 17 keypoints x (y coord, x coord, conf)
print("Shape of keypoints at each frame:", keypoints_timeseries[0].shape)



body_keypoints = ["nose", "left eye", "right eye", "left ear",
        "right ear", "left shoulder", "right shoulder", "left elbow",
        "right elbow", "left wrist", "right wrist", "left hip", "right hip",
        "left knee", "right knee", "left ankle", "right ankle"]