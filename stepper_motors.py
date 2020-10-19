import RPi.GPIO as GPIO
import time
from datetime import datetime
from multiprocessing import Process
from videoForSpyder import capture_and_send

def moveSpyder():
    print("MOTOR", datetime.now().strftime("%Y-%m-%d-%H:%M:%S"))
    GPIO.setmode(GPIO.BOARD)
    control_pins = [7,11,13,15]
    for pin in control_pins:
      GPIO.setup(pin, GPIO.OUT)
      GPIO.output(pin, 0)
    halfstep_seq = [
      [1,0,0,0],
      [1,1,0,0],
      [0,1,0,0],
      [0,1,1,0],
      [0,0,1,0],
      [0,0,1,1],
      [0,0,0,1],
      [1,0,0,1]
    ]
    for i in range(512):
      for halfstep in range(8):
        for pin in range(4):
          GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
        time.sleep(0.001)
    GPIO.cleanup()

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
    # moveSpyder()

