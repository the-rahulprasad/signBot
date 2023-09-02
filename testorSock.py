import os
import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.builders import model_builder
from object_detection.utils import config_util
import cv2
import numpy as np
import threading

from collections import Counter
import socket

os.chdir("../../../../")
print("Current dir: ",os.getcwd())
CUSTOM_MODEL_NAME = 'my_ssd_mobnet'
LABEL_MAP_NAME = 'label_map.pbtxt'

paths = {
    'ANNOTATION_PATH': os.path.join('Tensorflow', 'workspace','annotations'),
    'CHECKPOINT_PATH': os.path.join('Tensorflow', 'workspace','models',CUSTOM_MODEL_NAME),
 }

files = {
    'PIPELINE_CONFIG':os.path.join('Tensorflow', 'workspace','models', CUSTOM_MODEL_NAME, 'pipeline.config'),
    'LABELMAP': os.path.join(paths['ANNOTATION_PATH'], LABEL_MAP_NAME)
}

# Load pipeline config and build a detection model
configs = config_util.get_configs_from_pipeline_file(files['PIPELINE_CONFIG'])
detection_model = model_builder.build(model_config=configs['model'], is_training=False)

category_index = label_map_util.create_category_index_from_labelmap(files['LABELMAP'])

# Restore checkpoint
ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
ckpt.restore(os.path.join(paths['CHECKPOINT_PATH'], 'ckpt-3')).expect_partial()

# Define a global variable to store the latest frame
latest_frame = None
# Define an event object to signal threads to exit

prediction = []
num = 0


def most_frequent(lst):
    # Count the occurrences of each element in the list
    counts = Counter(lst)

    # Get the most common element and its count
    most_common = counts.most_common(1)[0][0]

    return most_common

def print_boxes_and_labels(detections, category_index,
                           label_id_offset=1, max_boxes_to_draw=5, min_score_thresh=.8):
    global prediction,num
    # Extract the detection results
    detection_boxes = detections['detection_boxes']
    detection_classes = detections['detection_classes'] + label_id_offset
    detection_scores = detections['detection_scores']

    # Iterate over the detected objects and print their details

    for i in range(min(max_boxes_to_draw, detection_boxes.shape[0])):
        if detection_scores[i] > min_score_thresh:
            class_name = category_index[detection_classes[i]]['name']
            prediction.append(class_name)

@tf.function
def detect_fn(image):
    image, shapes = detection_model.preprocess(image)
    prediction_dict = detection_model.predict(image, shapes)
    detections = detection_model.postprocess(prediction_dict, shapes)
    return detections


def receive_message():
    global flag,response
    while True:
        response = client_socket.recv(1024).decode('utf-8')
        print(response)

# create a thread to show the video feed from the camera
def show_video():
    global prediction,num
    # Open the default camera
    cap = cv2.VideoCapture(1)
    # startDetect = False
    global flag,response
    client_socket.sendall('started'.encode('utf-8'))
    while True:
        # Capture a frame
        ret, frame = cap.read()
        if not ret:
            break

        # Display the frame
        key=cv2.waitKey(1)
        if key == ord('q'):
            break
        elif response == 'reply':
            # startDetect = True
            # response = 'a'
            #
            # if startDetect:
            print("Started Recording")
            for _ in range(15):
                ret, frame = cap.read()
                image_np = np.array(frame)
                input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)
                detections = detect_fn(input_tensor)
                num_detections = int(detections.pop('num_detections'))
                detections = {key: value[0, :num_detections].numpy()
                              for key, value in detections.items()}

                detections['num_detections'] = num_detections
                # detection_classes should be ints.
                detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

            #num += 1
                print_boxes_and_labels(detections, category_index,
                                   label_id_offset=1, max_boxes_to_draw=5, min_score_thresh=.8)

            ans = 'Nothing'
            if len(prediction) > 0:
                #print(prediction)
                ans = most_frequent(prediction)
                if ans is not None:
                    print("Answer: ", ans)
                    client_socket.sendall(ans.encode('utf-8'))
                prediction.clear()
                # startDetect= False
                # num = 0



        cv2.imshow('frame', frame)

    cap.release()
    cv2.destroyAllWindows()



if __name__ == '__main__':
    # Define the size of the frame
    d_frame_width = 640
    d_frame_height = 480

    # Create a black dummy frame
    d_frame = np.zeros((d_frame_height, d_frame_width, 3), dtype=np.uint8)

    input_tensor = tf.convert_to_tensor(np.expand_dims(d_frame, 0), dtype=tf.float32)
    detections = detect_fn(input_tensor)
    # create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # get local machine name
    host = socket.gethostname()

    # connect to the server on a well-known port
    client_socket.connect((host, 12345))

    flag = 'a'
    response = 'a'

    # start both threads
    threading.Thread(target=receive_message).start()
    threading.Thread(target=show_video).start()




