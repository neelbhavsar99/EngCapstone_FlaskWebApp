import cv2
from imutils.video import WebcamVideoStream


class VideoCamera(object):

    #SRC= 0 is system, start turns on camera
    def __init__(self):
        self.stream = WebcamVideoStream(src=1).start()

    #Stop the webcam
    def __del__(self):
        self.stream.stop()

    #Collect the images in the form of an array
    def get_frame(self):
        image = self.stream.read()  #Automatically collect image and read it

        #these variables will be sent to the other forms as "data" variable
        ret, jpeg = cv2.imencode('.jpg', image)
        data = []
        data.append(jpeg.tobytes())
        return data