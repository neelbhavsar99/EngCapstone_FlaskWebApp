import time
import json
import _thread
from adafruit_motor import stepper
import board
from adafruit_motorkit import MotorKit
from urllib.request import urlopen
from urllib.error import HTTPError

kit = MotorKit(i2c=board.I2C())

url = "http://172.20.10.6:5000/move"
mode = ""
direction = ""
startX = ""
endX = ""


def movement():
    global mode, direction, startX, endX
    while (True):
        try:
            if mode == "Free Scanning Mode":
                while(direction == "right"):
                    kit.stepper1.onestep(
                        direction=stepper.FORWARD, style=stepper.DOUBLE)
                    time.sleep(0.04)
                while(direction == "left"):
                    kit.stepper1.onestep(
                        direction=stepper.BACKWARD, style=stepper.DOUBLE)
                    time.sleep(0.04)
            else:
                if (direction == "right"):
                    while(True):
                        if(endX < 400):
                            break
                        kit.stepper1.onestep(
                            direction=stepper.FORWARD, style=stepper.DOUBLE)
                        time.sleep(0.04)
                if (direction == "left"):
                    while(True):
                        if(startX > 0):
                            break
                        kit.stepper1.onestep(
                            direction=stepper.BACKWARD, style=stepper.DOUBLE)
                        time.sleep(0.04)
        except HTTPError as e:
            content = e.read()


def apiCaller():
    global mode, direction, startX, endX

    while(True):
        page = urlopen(url)
        html = page.read().decode("utf-8")
        json_data = json.loads(html)
        mode = json_data["Mode"]
        direction = json_data["Direction"]
        if mode == "Tracking Mode":
            startX = float(json_data["StartX"])
            endX = float(json_data["EndX"])
        print(
            f"Mode: {mode} Direction: {direction} startX: {startX} endX: {endX}")


if __name__ == "__main__":

    try:
        _thread.start_new_thread(apiCaller, ())
        _thread.start_new_thread(movement, ())
    except:
        print("Error: unable to start thread")


#
# #"""Simple test for using adafruit_motorkit with a stepper motor"""
# import time
# import json
# from adafruit_motor import stepper
# import board
# from adafruit_motorkit import MotorKit
# from urllib.request import urlopen
# from urllib.error import HTTPError
#
# kit = MotorKit(i2c=board.I2C())
# multiplier = 1.0
#
# url = "http://172.20.10.6:5000/move"
#
# def leftMovement(multiplier):
#             for i in range(1):
#                 kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
#                 time.sleep(multiplier*0.01)
#
#
# def rightMovement(multiplier):
#             for i in range(1):
#                 kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
#                 time.sleep(multiplier*0.01)
#
#
# def slightLeftMovement(multiplier):
#             for i in range(1):
#                 kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
#                 time.sleep(multiplier*0.01)
#
# def slightRightMovement(multiplier):
#             for i in range(1):
#                 kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
#                 time.sleep(multiplier*0.01)
#
#
# while (True):
#     try:
#         page = urlopen(url)
#         html = page.read().decode("utf-8")
#         print(html)
#         json_data = json.loads(html)
#
#         startX = float(json_data["StartX"])
#         endX = float(json_data["EndX"])
#         #print(startX)
#         #print(endX)
#
#
#
#         middle = (endX + startX)/2
#         print(middle)
#
#
#         if middle <= 40:
#             print("Condition 1")
#             rightMovement(1)
#
#
#         if middle > 40 and middle <= 80:
#             print("Condition 2")
#             rightMovement(1)
#
#         if middle > 80 and middle <= 160:
#             print("Condition 3")
#             rightMovement(1)
#
#
#
#
#
#
#         if middle > 240 and middle <= 310:
#             print("Condition 6")
#
#             leftMovement(1)
#
#         if middle > 310 and middle <= 360:
#             print ("Condition 7")
#             leftMovement(1)
#
#         if middle > 360:
#             print ("Condition 8")
#             leftMovement(1)
#
#
#     except HTTPError as e:
#         content = e.read()
#
#
#
#


#
# #"""Simple test for using adafruit_motorkit with a stepper motor"""
# import time
# import json
# from adafruit_motor import stepper
# import board
# from adafruit_motorkit import MotorKit
# from urllib.request import urlopen
# from urllib.error import HTTPError
#
# kit = MotorKit(i2c=board.I2C())
# multiplier = 1.0
#
# url = "http://10.0.0.97:5000/move"
#
# def leftMovement(multiplier):
#             for i in range(10):
#                 kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
#                 time.sleep(multiplier*0.01)
#
#
# def rightMovement(multiplier):
#             for i in range(10):
#                 kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
#                 time.sleep(multiplier*0.01)
#
#
# def slightLeftMovement(multiplier):
#             for i in range(6):
#                 kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
#                 time.sleep(multiplier*0.011)
#
# def slightRightMovement(multiplier):
#             for i in range(6):
#                 kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
#                 time.sleep(multiplier*0.011)
#
#
# while (True):
#     try:
#         page = urlopen(url)
#         html = page.read().decode("utf-8")
#         print(html)
#         json_data = json.loads(html)
#
#         startX = float(json_data["StartX"])
#         endX = float(json_data["EndX"])
#         #print(startX)
#         #print(endX)
#
#
#
#         middle = abs(endX - startX)/2
#         print(middle)
#
#
#         if middle > 0 and middle < 20:
#             print("Condition 1")
#             rightMovement(0.8)
#
#
#         if middle > 20 and middle < 40:
#             print("Condition 2")
#             rightMovement(1)
#
#         if middle > 40 and middle < 50:
#             print("Condition 2")
#             slightRightMovement(1)
#
#
#
#         if middle > 70 and middle < 100:
#             print ("New Test Middle")
#             slightLeftMovement(1)
#
#         if middle > 100 and middle < 120:
#             print("Condition 5")
#
#             leftMovement(1)
#
#         if middle > 120 and middle < 140:
#             print ("Condition 6")
#             leftMovement(1)
#
#         if middle > 140 and middle < 160:
#             print ("Condition 6")
#             leftMovement(1.5)
#
#
#     except HTTPError as e:
#         content = e.read()
