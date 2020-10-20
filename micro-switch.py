# curl -sL https://github.com/Seeed-Studio/grove.py/raw/master/install.sh | sudo bash -s -
import time
from multiprocessing import Process
import RPi.GPIO as GPIO
from videoForSpyder import capture_and_send
from stepper_pi import loopSpyder

PIN = 5

def runInParallel(*fns):
  proc = []
  for fn in fns:
    p = Process(target=fn)
    p.start()
    proc.append(p)
  for p in proc:
    p.join()

def main():
    capture = False

    while True:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN, GPIO.IN)
        if GPIO.input(PIN) is 1 and capture is not True:
            print("on")
            # runInParallel(capture_and_send, loopSpyder)
            loopSpyder()
            capture = True
        elif GPIO.input(PIN) is 0:
            print("off")
            capture = False
        time.sleep(1)


if __name__ == '__main__':
    main()

