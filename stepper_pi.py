import RPi.GPIO as gpio
import time
from datetime import datetime
from multiprocessing import Process
from videoForSpyder import capture_and_send
import argparse

DIR = 13
PUL = 12

rotations = 1440
direction = "cw"

##TODO Include start position
def moveSpyder():
    #gpio.BCM for physical pin numbers
    gpio.setmode(gpio.BCM) 
    gpio.setwarnings(False)
    gpio.setup([PUL, DIR], gpio.OUT)
    gpio.output(DIR, gpio.HIGH)

    pwmPUL = gpio.PWM(PUL, 300)
    pwmPUL.start(0)

    """
         To rotate the mechanical claw, you need to specify the rotation angle and direction
         :param angle: integer data, rotation angle
         :param direction: string data, rotation direction, value: "ccw" or "cw". ccw: counterclockwise rotation, cw: clockwise rotation
    :return:None
    """
    if direction == "ccw":
        gpio.output(DIR, gpio.LOW)
    elif direction == "cw":
        gpio.output(DIR, gpio.HIGH)
    else:
        return
    pwmPUL.ChangeDutyCycle(50)
    #time.sleep(2)
    time.sleep(rotations/360)

    #processify(capture_and_send())
#    subprocess.run(['python3', 'videoForSpyder.py'])

## Don't be dependent on time, sync video with motor
    pwmPUL.stop()
    gpio.cleanup()

def runInParallel(*fns):
  proc = []
  for fn in fns:
    p = Process(target=fn)
    p.start()
    proc.append(p)
  for p in proc:
    p.join()

if __name__ == '__main__':
    runInParallel(capture_and_send, moveSpyder)

    # moveSpyder(rotations, direction)