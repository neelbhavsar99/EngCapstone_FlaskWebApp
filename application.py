# PYTHON APP: python3 application.py
from imutils.video import VideoStream
from flask import Flask, Response, make_response, render_template, request, jsonify
from constants import LABELS, COLORS
import cv2
import imutils
import argparse
import numpy as np
import os


templateDirectory = os.path.abspath('templates')
staticDirectory = os.path.abspath('static')
application = Flask(__name__, template_folder=templateDirectory,
                    static_folder=staticDirectory)

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
# camera = VideoStream("http://10.0.0.117:8080/video").start() # Uncomment line  to use phone camera

# Loading Caffe Model
print('[Status] Loading Model...')
nn = cv2.dnn.readNetFromCaffe(args.prototxt, args.model)

latest_prediction = None

# grab the width, height, and fps of the frames in the video stream.
frameWidth = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
frameHeight = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
streamFps = int(camera.get(cv2.CAP_PROP_FPS))
print(f"FPS: {streamFps}, frameWidth: {frameWidth}, frameHeight: {frameHeight}")

# ISSUE HERE TO OVERWRITE PREVIOUS RECORDING restart to record second video
# initialize the FourCC and a video writer object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
# Actual fps count is much lower, must check and fix!
output = cv2.VideoWriter('output.avi', fourcc, streamFps/3,
                         (frameWidth, frameHeight))


def get_predictions(frame):
    predictions = []

    # Converting Frame to Blob
    blob = cv2.dnn.blobFromImage(cv2.resize(
        frame, (300, 300)), 0.007843, (300, 300), 127.5)

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
            predictions.append(
                {"ID": idx, "Confidence": confidence * 100, "Box": box.astype("int")})

    return sorted(predictions, key=lambda i: i['Confidence'])


def generate_frame():
    global latest_prediction, startRecording, saveRecording

    # Initialize Video Stream
    print('[Status] Starting Video Stream...')

    # Loop Video Stream
    while True:
        # print(f"startRecording: {startRecording}, saveRecording: {saveRecording}")
        success, frame = camera.read()  # Read camera frame continuosly
        # frame = camera.read()         # Uncomment line to use phone camera
        if startRecording:
            output.write(frame)

        # Resize Frame to 400 pixels
        frame = imutils.resize(frame, width=400)

        predictions = get_predictions(frame)

        if predictions:
            latest_prediction = predictions[0]

            # Computing the (x,y) - coordinates of the bounding box
            startX, startY, endX, endY = latest_prediction["Box"].astype("int")
            # Drawing the prediction and bounding box
            label = "{}: {:.2f}%".format(
                LABELS[latest_prediction["ID"]].capitalize(), latest_prediction["Confidence"])

            cv2.rectangle(frame, (startX, startY), (endX, endY),
                          COLORS[latest_prediction["ID"]], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, COLORS[latest_prediction["ID"]], 2)

        # encode frame into multiple pics
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()  # computer vision requires this
        frame = (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' +
                 frame + b'\r\n')

        yield frame
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        if saveRecording == True:
            output.release()
            print("Stop Recording...")
            startRecording = False
            saveRecording = False

    camera.release()
    cv2.destroyAllWindows()


@application.before_first_request
def OnceAndOnlyOnce():
    global selectedMode, selectedDirection, startX, endX, startRecording, saveRecording
    selectedMode = "Tracking Mode"
    selectedDirection = "Stop"
    startX = 50
    endX = 350
    startRecording = False
    saveRecording = False


@application.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        global selectedMode, selectedDirection, startX, endX, startRecording, saveRecording

        startRecording = request.json.get("startRecording")
        saveRecording = request.json.get("saveRecording")
        modeVal = request.json.get("mode")
        selectedDirection = request.json.get("direction")

        if modeVal == 1:
            selectedMode = "Free Scanning Mode"
        elif modeVal == 0:
            selectedMode = "Tracking Mode"

        # return jsonify({"data": {"val": modeVal}})
    return render_template("index.html")


@application.route('/video')
def video():
    return Response(generate_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


@application.route('/move')
def direction():
    global selectedMode, selectedDirection
    startX, startY, endX, endY = latest_prediction["Box"].astype("int")

    if selectedMode == "Free Scanning Mode":
        return jsonify({"Mode": selectedMode, "Direction": selectedDirection})
    else:
        if LABELS[latest_prediction["ID"]] == "person" and startX > 40 and endX < 360:
            direction = "none"
        elif LABELS[latest_prediction["ID"]] == "person" and startX < 40:
            direction = "left"
        elif LABELS[latest_prediction["ID"]] == "person" and endX > 360:
            direction = "right"
        else:
            direction = ""
        return jsonify({"Mode": selectedMode, "Direction": direction, "StartX": str(startX), "EndX": str(endX)})


if __name__ == "__main__":
    application.run(host="0.0.0.0")
