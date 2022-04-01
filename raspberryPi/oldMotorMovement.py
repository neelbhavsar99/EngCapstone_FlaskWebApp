

#"""Simple test for using adafruit_motorkit with a stepper motor"""
import time
import json
from adafruit_motor import stepper
import board
from adafruit_motorkit import MotorKit
from urllib.request import urlopen
from urllib.error import HTTPError

kit = MotorKit(i2c=board.I2C())
multiplier = 1.0

url = "http://172.20.10.6:5000/move"

def leftMovement(multiplier): 
            for i in range(10):
                kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
                time.sleep(multiplier*0.02)
                break
        
def rightMovement(multiplier):
            for i in range(10):
                kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
                time.sleep(multiplier*0.02)
                break

def slightLeftMovement(multiplier):
            for i in range(2):
                kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
                time.sleep(multiplier*0.03)
                break
def slightRightMovement(multiplier):
            for i in range(2):
                kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
                time.sleep(multiplier*0.03)
                break
            
while (True):
    try:
        page = urlopen(url)
        html = page.read().decode("utf-8")
        print(html)
        json_data = json.loads(html)
        
        startX = float(json_data["StartX"])
        endX = float(json_data["EndX"])
        #print(startX)
        #print(endX)
        

        
        middle = abs(endX - startX)/2
        print(middle)
        

        if middle > 0 and middle < 20:
            print("Condition 1")
            rightMovement(1)
            
            
        if middle > 20 and middle < 40:
            print("Condition 2")
            rightMovement(2.5)
        
        if middle > 40 and middle < 50:
            print("Condition 2")
            slightRightMovement(2.7)
        
            
               
        if middle > 70 and middle < 100:
            print ("New Test Middle")
            slightLeftMovement(2.7)
            
        if middle > 100 and middle < 120:
            print("Condition 5")

            leftMovement(2.7)
            
        if middle > 120 and middle < 140:
            print ("Condition 6")
            leftMovement(2.5)
        
        if middle > 140 and middle < 160:
            print ("Condition 6")
            leftMovement(1)
  

    except HTTPError as e:
        content = e.read()






#OLD CODE
# 
# """Simple test for using adafruit_motorkit with a stepper motor"""
# import time
# from adafruit_motor import stepper
# import board
# from adafruit_motorkit import MotorKit
# from urllib.request import urlopen
# from urllib.error import HTTPError
# 
# kit = MotorKit(i2c=board.I2C())
# 
# 
# url = "http://10.0.0.89:5000/move"
# 
# 
# while (True):
#     try:
#         page = urlopen(url)
#         html = page.read().decode("utf-8")
# #         start_index = html.find("<body>") + len("<body>")
# #         end_index = html.find("</body>")
# #         title = html[start_index:end_index]
# #         print(title)
#         if (html.find('right') != -1):
#             for i in range(10):
#                 kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
#                 time.sleep(0.05)
#     
#         if (html.find('left') != -1):
#             for i in range(10):
#                 kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
#                 time.sleep(0.05)     
# 
#     except HTTPError as e:
#         content = e.read()
#     


