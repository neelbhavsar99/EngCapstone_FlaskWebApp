#GITHUB LINK: https://github.com/krishnaik06/Flask-Web-Framework/tree/main/Tutorial%207%20opencv
from flask import Flask, render_template, Response
import cv2  #Open source computer vision library

app = Flask(__name__)
camera = cv2.VideoCapture(0)


def generate_frame():
    while True:
        success, frame = camera.read()  #read camera frame continuosly
        if not success:
            break
        else:
            #Using HAAR Cascade data cloned from cv2 GitHub
            detector = cv2.CascadeClassifier(
                "/Users/neelbhavsar/Desktop/Programming/capstoneproj/Haarcascades/haarcascade_frontalface_default.xml"
            )
            eye_cascade = cv2.CascadeClassifier(
                "/Users/neelbhavsar/Desktop/Programming/capstoneproj/Haarcascades/haarcascade_eye.xml"
            )
            #Get face coordinates
            faces = detector.detectMultiScale(frame, 1.1, 7)
            gray = cv2.cvtColor(
                frame, cv2.COLOR_BGR2GRAY
            )  #Convert color of frame from BGR to Grayscale

            #test = detector.load(
            #    '/Users/neelbhavsar/Desktop/Programming/capstoneproj/Haarcascades/haarcascade_frontalface_default.xml'
            #)
            #print("Hello")
            #print(test)

            #Draw the rectangle around each face#provide two coordinates for bounding box
            for (x, y, w, h) in faces:
                #225,0,0 bounding box color
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                roi_gray = gray[y:y + h, x:x + w]
                roi_color = frame[y:y + h, x:x + w]
                #Doing the same thing for eyes now
                eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 3)
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh),
                                  (0, 255, 0), 2)

            #encode frame into multiple pics
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()  #computer vision requires this
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


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