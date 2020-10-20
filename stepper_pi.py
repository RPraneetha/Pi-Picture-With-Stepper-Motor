import RPi.GPIO as gpio
import time
from multiprocessing import Process
from videoForSpyder import capture_and_send
import argparse

DIR = 13
PUL = 12

rotations = 4000
direction = "ccw"

def loopSpyder():
    global rotations, direction
    print(direction, rotations)
    moveSpyder()
    direction = "ccw" if direction == "cw" else "cw"
    print(direction, rotations)
    moveSpyder()
    direction = "ccw" if direction == "cw" else "cw"

##TODO Include start position
def moveSpyder():
    global rotations, direction
    #gpio.BCM for physical pin numbers
    gpio.setmode(gpio.BCM) 
    gpio.setwarnings(False)
    gpio.setup([PUL, DIR], gpio.OUT)
    gpio.output(DIR, gpio.HIGH)

    pwmPUL = gpio.PWM(PUL, 1000) #800, 1000
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

    args = parser.parse_args()

    rotations = args.rotations if args.rotations else 100
    direction = args.direction if args.direction else "ccw"

    #runInParallel(capture_and_send, moveSpyder)
    moveSpyder()
    # direction = "ccw" if direction == "cw" else "cw"
    # moveSpyder()

