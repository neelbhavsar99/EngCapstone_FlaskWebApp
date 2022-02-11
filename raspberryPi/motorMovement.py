

"""Simple test for using adafruit_motorkit with a stepper motor"""
import time
from adafruit_motor import stepper
import board
from adafruit_motorkit import MotorKit
from urllib.request import urlopen
from urllib.error import HTTPError

kit = MotorKit(i2c=board.I2C())


url = "http://10.0.0.2:5000/move"


while (True):
    try:
        page = urlopen(url)
        html = page.read().decode("utf-8")
        start_index = html.find("<body>") + len("<body>")
        end_index = html.find("</body>")
        title = html[start_index:end_index]
        print(title)
        if (title.find('left') != -1):
            for i in range(10):
                kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
                time.sleep(0.01)
    
        if (title.find('right') != -1):
            for i in range(10):
                kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
                time.sleep(0.01)     

    except HTTPError as e:
        content = e.read()

    

        
    

