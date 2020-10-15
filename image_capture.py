#!/usr/bin/env python3

import os
import subprocess
import argparse
from datetime import datetime

from config import (
    RESOLUTION, CAM_COUNT, IMAGE_PATH, FRIDGE_NAME, REMOTE_ADDRESS, REMOTE_PATH, REMOTE_USER
)
from stepper_pi import moveSpyder

_remote = '{}@{}'.format(REMOTE_USER, REMOTE_ADDRESS)
_remote_path = '{}/{}'.format(REMOTE_PATH, FRIDGE_NAME)

print("Creating remote image path...")
subprocess.run(['ssh', _remote, 'mkdir', '-p', _remote_path])

_zip = None
if not os.path.exists(IMAGE_PATH):
    os.mkdir(IMAGE_PATH)

def _get_image_name(number):
    return 'nano_image_test{}.jpg'.format(number)

def send_images(file):
    print('Transferring images...')

    path = './{}'.format(file)
    remote = '{}:{}'.format(_remote, _remote_path)
    print(path, remote)
    subprocess.run(['scp', path, remote])

def zip_images(name):
    dir_before = os.getcwd()
    path = '{}/{}'.format(dir_before, name)
    os.chdir(path)

    print('Zipping images...')

    try:
        files = [_get_image_name(i) for i in range(CAM_COUNT)]
        dest = '{}_{}.zip'.format(FRIDGE_NAME, datetime.now().strftime("%Y-%m-%d-%H:%M:%S"))
        subprocess.run(['zip', '-9', dest] + files)
    except Exception:
        print("Something went wrong while zipping")
        return None

    return dest

def capture_and_send():
    capture_images()

    _zip = zip_images(IMAGE_PATH)

    if _zip is not None:
        send_images(_zip)

    print('Done.')

def capture_images():

    print('Capturing images...')

    processes = []

    for i in range(CAM_COUNT):
        command = ['fswebcam',
                   '-d', '/dev/video{}'.format(i),
                   '-r', RESOLUTION,
                   '--title', _get_image_name(i),
                   '--rotate', '90',
                   '-q',
                   '{}/{}'.format(IMAGE_PATH, _get_image_name(i))
                   ]
        # oscommand = ' '.join(map(str,command))
        # os.system(oscommand)
        processes.append(subprocess.Popen(command))

    [process.wait() for process in processes]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pass arguments to control motor.')
    parser.add_argument('--rotations', '-r', type=int, help='Number of rotations')
    parser.add_argument('--direction', '-d', type=str, help='Direction of the motor. cw for clockwise(upwards), '
                                                  'ccw for counter-clockwise(downwards)')

    args = parser.parse_args()

    rotations = args.rotations if args.rotations else 1440
    direction = args.direction if args.direction else "cw"

    moveSpyder(rotations, direction)
    capture_and_send()
