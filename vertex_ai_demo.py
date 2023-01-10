import os
import tensorflow as tf
import cv2
from google.cloud import aiplatform
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value
from typing import Dict, List, Union


# Adapted from https://github.com/googleapis/python-aiplatform/blob/main/samples/snippets/prediction_service/predict_custom_trained_model_sample.py
def vertex_ai_predict(instances: Union[Dict, List[Dict]], client, endpoint):

    # jsonify inputs
    instances = [json_format.ParseDict(instances[0], Value())]

    # Query model on VertexAI
    response = client.predict(endpoint=endpoint, instances=instances)

   # The predictions are a google.protobuf.Value representation of the model's predictions.
    return response.predictions


def load_vertex_ai_client(api_endpoint: str):

    # This client only needs to be initialized once, and can be reused for multiple requests.
    client = aiplatform.gapic.PredictionServiceClient(client_options={"api_endpoint": api_endpoint})
    return client


def movenet(video_filepath):

    # Load VertexAI info from environment
    project = os.environ['GCLOUD_PROJECT_ID']
    endpoint_id = os.environ["VERTEX_AI_ENDPOINT_ID"]
    location = os.environ["VERTEX_AI_LOCATION"]
    api_endpoint = os.environ["VERTEX_AI_API_ENDPOINT"]

    print("\n")
    print("----------------------------------------------")
    print("Initializing VertexAI client")
    print("----------------------------------------------")

    # Initialize VertexAI client
    client = load_vertex_ai_client(api_endpoint)
    endpoint = f"projects/{project}/locations/{location}/endpoints/{endpoint_id}"

    cap = cv2.VideoCapture(video_filepath)

    print("\n")
    print("----------------------------------------------")
    print(f"Reading video file from {video_filepath}")
    print("----------------------------------------------")

    while cap.isOpened():

        status, frame = cap.read()

        # All video frames have been read
        if frame is None:
            print("\n")
            print("----------------------------------------------")
            print("All video frames analyzed")
            print("----------------------------------------------")
            break

        # Resize frame dims to multiple of 32 and longer side 256
        img = frame.copy()
        img = tf.image.resize_with_pad(tf.expand_dims(img, axis=0), 128,256)

        # Cast to 32-bit int representation
        img = tf.cast(img, dtype=tf.int32)

        # Represent input as a list for python client api
        img_list = img.numpy().tolist()

        print("\n")
        print("----------------------------------------------")
        print("Connecting to VertexAI to get prediction")
        print("----------------------------------------------")

        # Get prediction
        results = vertex_ai_predict( instances=img_list, client=client,\
                                     endpoint=endpoint)

        print("\n")
        print("----------------------------------------------")
        print("Prediction received")
        print("----------------------------------------------")


    cap.release()


if __name__ == "__main__":
     movenet('test.mp4')