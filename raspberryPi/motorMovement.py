

"""Simple test for using adafruit_motorkit with a stepper motor"""
import time
import json
# from adafruit_motor import stepper
# import board
# from adafruit_motorkit import MotorKit
from urllib.request import urlopen
from urllib.error import HTTPError

# kit = MotorKit(i2c=board.I2C())
multiplier = 1

url = "http://10.17.27.161:5000/move"

x = 0
while (True):
    try:
        page = urlopen(url)
        html = page.read().decode("utf-8")
        print(type(html))
        json_data = json.loads(html)
        
        startX = float(json_data["StartX"])
        endX = float(json_data["EndX"])

        
        # print (f"Start X: {startX}\n End X: {endX} ")

        # x += 1
        # time.sleep(0.1)
        # if x == 50:
        #     break
        
        middle = (endX - startX)/2

        if middle > 200 and middle < 250:
            LeftMovement(3)
            
        elif middle > 250 and middle < 300:
            LeftMovement(2)
        
        elif middle > 300 and middle < 400:
            LeftMovement(1)
           
        
        elif middle > 150 and middle < 200:
            RightMovement(3)
            
        elif middle > 200 and middle < 100:
            RightMovement(2)
        
        elif middle > 100 and middle < 0:
            RightMovement(1)

        

        # if startX > 40 and endX < 360:
        #     direction = "none"
        # elif startX < 40:
        #     for i in range(10):
        #         kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
        #         time.sleep(0.01)
        #     direction = "left"
        # elif endX > 360:
        # #     for i in range(10):
        # #         kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
        # #         time.sleep(0.01)   
        #     direction = "right"
        # else:
        #     direction = ""
        
        
        # if (title.find('left') != -1):
        #     for i in range(10):
        #         kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
        #         time.sleep(0.01)
    
        # if (title.find('right') != -1):
        #     for i in range(10):
        #         kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
        #         time.sleep(0.01)     

    except HTTPError as e:
        content = e.read()

    def LeftMovement(multiplier): 
            for i in range(10):
                kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
                time.sleep(multiplier*0.01)
        
    def RightMovement(multiplier):
            for i in range(10):
                kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
                time.sleep(multiplier*0.01)

   
    
