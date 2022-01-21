#GITHUB LINK: https://github.com/krishnaik06/Flask-Web-Framework/tree/main/Tutorial%207%20opencv
## PYTHON APP: python3 app.py -p Caffe/SSD_MobileNet_prototxt.txt -m Caffe/SSD_MobileNet.caffemodel
## PYTHON APP: python3 detectDNN.py -p Caffe/SSD_MobileNet_prototxt.txt -m Caffe/SSD_MobileNet.caffemodel
## python3 real_time_object_detection.py -p Caffe/SSD_MobileNet_prototxt.txt -m Caffe/SSD_MobileNet.caffemodel

from flask import Flask, render_template, Response
import cv2  #Open source computer vision library

import cv2
import time
import imutils
import argparse
import numpy as np

from imutils.video import FPS
from imutils.video import VideoStream

app = Flask(__name__)
camera = cv2.VideoCapture(0)

# def generate_frame():
#     while True:
#         success, frame = camera.read()  #read camera frame continuosly
#         if not success:
#             break
#         else:
#             #Using HAAR Cascade data cloned from cv2 GitHub
#             detector = cv2.CascadeClassifier(
#                 "/Users/neelbhavsar/Desktop/Programming/capstoneproj/Haarcascades/haarcascade_frontalface_default.xml"
#             )
#             eye_cascade = cv2.CascadeClassifier(
#                 "/Users/neelbhavsar/Desktop/Programming/capstoneproj/Haarcascades/haarcascade_eye.xml"
#             )
#             #Get face coordinates
#             faces = detector.detectMultiScale(frame, 1.1, 7)
#             gray = cv2.cvtColor(
#                 frame, cv2.COLOR_BGR2GRAY
#             )  #Convert color of frame from BGR to Grayscale

#             #test = detector.load(
#             #    '/Users/neelbhavsar/Desktop/Programming/capstoneproj/Haarcascades/haarcascade_frontalface_default.xml'
#             #)
#             #print("Hello")
#             #print(test)

#             #Draw the rectangle around each face#provide two coordinates for bounding box
#             for (x, y, w, h) in faces:
#                 #225,0,0 bounding box color
#                 cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
#                 roi_gray = gray[y:y + h, x:x + w]
#                 roi_color = frame[y:y + h, x:x + w]
#                 #Doing the same thing for eyes now
#                 eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 3)
#                 for (ex, ey, ew, eh) in eyes:
#                     cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh),
#                                   (0, 255, 0), 2)

#             #encode frame into multiple pics
#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()  #computer vision requires this
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def generate_frame():
    #Constructing Argument Parse to input from Command Line
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-p",
        "--prototxt",
        required=True,
        help=
        '/Users/neelbhavsar/Desktop/Programming/capstoneproj/Caffe-SSD-Object-Detection-master/Object Detection Caffe/Caffe/SSD_MobileNet_prototxt.txt'
    )
    ap.add_argument(
        "-m",
        "--model",
        required=True,
        help=
        '/Users/neelbhavsar/Desktop/Programming/capstoneproj/Caffe-SSD-Object-Detection-master/Object Detection Caffe/Caffe/SSD_MobileNet.caffemodel'
    )
    ap.add_argument("-c", "--confidence", type=float, default=0.7)
    args = vars(ap.parse_args())

    #Initialize Objects and corresponding colors which the model can detect
    labels = [
        "background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus",
        "car", "cat", "chair", "cow", "diningtable", "dog", "horse",
        "motorbike", "person", "pottedplant", "sheep", "sofa", "train",
        "tvmonitor"
    ]
    colors = np.random.uniform(0, 255, size=(len(labels), 3))

    #Loading Caffe Model
    print('[Status] Loading Model...')
    nn = cv2.dnn.readNetFromCaffe(args['prototxt'], args['model'])
    #python3 detectDNN.py -p Caffe/SSD_MobileNet_prototxt.txt -m Caffe/SSD_MobileNet.caffemodel

    #Initialize Video Stream
    print('[Status] Starting Video Stream...')
    vs = VideoStream(src=1).start()
    time.sleep(2.0)
    fps = FPS().start()

    #Loop Video Stream
    while True:

        #Resize Frame to 400 pixels
        frame = vs.read()
        frame = imutils.resize(frame, width=400)
        (h, w) = frame.shape[:2]

        #Converting Frame to Blob
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843,
                                     (300, 300), 127.5)

        #Passing Blob through network to detect and predict
        nn.setInput(blob)
        detections = nn.forward()

        #Loop over the detections
        for i in np.arange(0, detections.shape[2]):

            #Extracting the confidence of predictions
            confidence = detections[0, 0, i, 2]

            #Filtering out weak predictions
            if confidence > args["confidence"]:

                #Extracting the index of the labels from the detection
                #Computing the (x,y) - coordinates of the bounding box
                idx = int(detections[0, 0, i, 1])

                #Extracting bounding box coordinates
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                #Drawing the prediction and bounding box
                label = "{}: {:.2f}%".format(labels[idx], confidence * 100)
                cv2.rectangle(frame, (startX, startY), (endX, endY),
                              colors[idx], 2)

                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(frame, label, (startX, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors[idx], 2)

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break
        fps.update()

    fps.stop()

    print("[Info] Elapsed time: {:.2f}".format(fps.elapsed()))
    print("[Info] Approximate FPS:  {:.2f}".format(fps.fps()))

    cv2.destroyAllWindows()
    vs.stop()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video')
def video():
    #Response will call some function
    return Response(generate_frame(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)
    #app.run()