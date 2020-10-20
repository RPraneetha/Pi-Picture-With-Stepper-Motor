import RPi.GPIO as gpio
import time
from multiprocessing import Process
from videoForSpyder import capture_and_send
import argparse

DIR = 13
PUL = 12

DOWNWARD_ROTATIONS = 4400
DOWNWARD_SPEED = 1000
UPWARD_ROTATIONS = 1000
UPWARD_SPEED = 8000
rotations = 1000 #4000
direction = "cw"

def loopSpyder():
    time.sleep(1)
    global rotations, direction
    moveSpyder(DOWNWARD_ROTATIONS, direction, DOWNWARD_SPEED)
    direction = "ccw" if direction == "cw" else "cw"
    moveSpyder(UPWARD_ROTATIONS, direction, UPWARD_SPEED)
    direction = "ccw" if direction == "cw" else "cw"

##TODO Include start position
def moveSpyder(rotations, direction, speed):
    #gpio.BCM for physical pin numbers
    gpio.setmode(gpio.BCM) 
    gpio.setwarnings(False)
    gpio.setup([PUL, DIR], gpio.OUT)
    gpio.output(DIR, gpio.HIGH)

    pwmPUL = gpio.PWM(PUL, speed) #800, 1000
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
    time.sleep(rotations/360)

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
    parser = argparse.ArgumentParser(description='Pass arguments to control motor.')
    parser.add_argument('--rotations', '-r', type=int, help='Number of rotations')
    parser.add_argument('--direction', '-d', type=str, help='Direction of the motor. cw for clockwise(downwards), '
                                                            'ccw for counter-clockwise(upwards)')
    parser.add_argument('--speed', '-s', type=int, help='Speed(frequency) of the motor')

    args = parser.parse_args()

    rotations = args.rotations if args.rotations else 100
    direction = args.direction if args.direction else "ccw"
    speed = args.speed if args.speed else 1000

    #runInParallel(capture_and_send, moveSpyder)
    moveSpyder(rotations, direction, speed)
    # direction = "ccw" if direction == "cw" else "cw"
    # loopSpyder()

