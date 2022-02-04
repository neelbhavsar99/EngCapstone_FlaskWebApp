#GITHUB LINK: https://github.com/krishnaik06/Flask-Web-Framework/tree/main/Tutorial%207%20opencv
## PYTHON APP: python3 app.py -p Caffe/SSD_MobileNet_prototxt.txt -m Caffe/SSD_MobileNet.caffemodel
## PYTHON APP: python3 detectDNN.py -p Caffe/SSD_MobileNet_prototxt.txt -m Caffe/SSD_MobileNet.caffemodel
## python3 real_time_object_detection.py -p Caffe/SSD_MobileNet_prototxt.txt -m Caffe/SSD_MobileNet.caffemodel

import cv2
import imutils
import argparse
import numpy as np
import os
from imutils.video import FPS

from flask import Flask, Response, make_response, render_template, request, jsonify

from constants import LABELS, COLORS

template_dir = os.path.abspath('templates')
static_dir = os.path.abspath('static')
application = Flask(__name__, template_folder=template_dir,
                    static_folder=static_dir)

ARG_PARSE = argparse.ArgumentParser()
ARG_PARSE.add_argument(
    "-p",
    "--prototxt",
    metavar="filename",
    default="./server/Caffe/SSD_MobileNet_prototxt.txt",
    help="Protottx Path"
)
ARG_PARSE.add_argument(
    "-m",
    "--model",
    metavar="filename",
    default="./server/Caffe/SSD_MobileNet.caffemodel",
    help="Model Path"
)
ARG_PARSE.add_argument(
    "-c", 
    "--confidence", 
    type=float, 
    default=0.7,
    help="Set the confidence"
)

args = ARG_PARSE.parse_args()

camera = cv2.VideoCapture(0)

print("Prototxt Path: " + str(args.prototxt))
print("Model Path: " + str(args.model))

# Loading Caffe Model
print('[Status] Loading Model...')
nn = cv2.dnn.readNetFromCaffe(args.prototxt, args.model)

latest_prediction = None

def get_predictions(frame):
    predictions = []
    
    # Converting Frame to Blob
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843,
                                (300, 300), 127.5)

    # Passing Blob through network to detect and predict
    nn.setInput(blob)
    detections = nn.forward()

    # Loop over the detections
    for i in np.arange(0, detections.shape[2]):
        # Extracting the confidence of predictions
        confidence = detections[0, 0, i, 2]

        # Filtering out weak predictions
        if confidence > args.confidence:
            # Extracting the index of the labels from the detection
            idx = int(detections[0, 0, i, 1])
            # Extracting bounding box coordinates
            h, w = frame.shape[:2]
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            # Appending to predictions
            predictions.append({"ID": idx, "Confidence": confidence * 100, "Box": box.astype("int")})

    return sorted(predictions, key = lambda i: i['Confidence'])

def generate_frame():
    global latest_prediction
    #Initialize Video Stream
    print('[Status] Starting Video Stream...')
    fps = FPS().start()

    # Loop Video Stream
    while True:
        success, frame = camera.read()  # Read camera frame continuosly
        # Resize Frame to 400 pixels
        frame = imutils.resize(frame, width=400)
        
        predictions = get_predictions(frame)
        
        if predictions:
            latest_prediction = predictions[0]
            
            # Computing the (x,y) - coordinates of the bounding box
            startX, startY, endX, endY = latest_prediction["Box"].astype("int")
            # Drawing the prediction and bounding box
            label = "{}: {:.2f}%".format(LABELS[latest_prediction["ID"]].capitalize(), latest_prediction["Confidence"])
            
            cv2.rectangle(frame, (startX, startY), (endX, endY), COLORS[latest_prediction["ID"]], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX,0.5, COLORS[latest_prediction["ID"]], 2)

        #encode frame into multiple pics
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()  #computer vision requires this
        frame = (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
        yield frame
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

        fps.update()

    fps.stop()

    print("[Info] Elapsed time: {:.2f}".format(fps.elapsed()))
    print("[Info] Approximate FPS:  {:.2f}".format(fps.fps()))

    cv2.destroyAllWindows()

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/video')
def video():
    return Response(generate_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

@application.route('/move')
def direction():
    startX, startY, endX, endY = latest_prediction["Box"].astype("int")
    
    if LABELS[latest_prediction["ID"]] == "person" and startX > 40 and endX < 360:
        mode = "stop"
        direction = "none"
    elif LABELS[latest_prediction["ID"]]== "person" and startX < 40:                        
        mode = "track"
        direction = "left"
    elif LABELS[latest_prediction["ID"]] == "person" and endX > 360:
        mode = "track"
        direction = "right"
    
    return jsonify({"Mode": mode, "Direction": direction})

if __name__ == "__main__":
    application.run(host="0.0.0.0", debug=True)