# curl -sL https://github.com/Seeed-Studio/grove.py/raw/master/install.sh | sudo bash -s -
import time
import sys
from multiprocessing import Process
from grove.gpio import GPIO
from videoForSpyder import capture_and_send
from stepper_pi import moveSpyder
# from stepper_motors import moveSpyder

class GroveTiltSwitch(GPIO):
    def __init__(self, pin):
        super(GroveTiltSwitch, self).__init__(pin, GPIO.IN)

    @property
    def state(self):
        return super(GroveTiltSwitch, self).read()

def runInParallel(*fns):
  proc = []
  for fn in fns:
    p = Process(target=fn)
    p.start()
    proc.append(p)
  for p in proc:
    p.join()

def main():
    if len(sys.argv) < 2:
        print('Usage: {} pin'.format(sys.argv[0]))
        sys.exit(1)

    # swicth = GroveTiltSwitch(int(sys.argv[1]))

    while True:
        # if swicth.state is 1:
        if True:
            print("on")
            # runInParallel(capture_and_send(), moveSpyder())
            runInParallel(capture_and_send(), moveSpyder(1440, "cw"))
        else:
            print("off")
        time.sleep(1)


if __name__ == '__main__':
    main()

