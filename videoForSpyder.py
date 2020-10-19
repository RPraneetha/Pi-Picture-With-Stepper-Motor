#!/usr/bin/env python3

import os
import subprocess
from config import (
    RESOLUTION, CAM_COUNT, VIDEO_PATH, FRIDGE_NAME, REMOTE_ADDRESS, REMOTE_PATH, REMOTE_USER, VIDEO_DURATION, FRAME_RATE
)
from datetime import datetime

_remote = '{}@{}'.format(REMOTE_USER, REMOTE_ADDRESS)
_remote_path = '{}/{}'.format(REMOTE_PATH, FRIDGE_NAME)

print("Creating remote video path...")
subprocess.run(['ssh', _remote, 'mkdir', '-p', _remote_path])

_zip = None
if not os.path.exists(VIDEO_PATH):
    os.mkdir(VIDEO_PATH)

def _get_video_name(number):
    return 'nano_video_test{}.avi'.format(number)

def send_videos(file):
    print('Transferring images...')
    
    path = './{}'.format(file)
    remote = '{}:{}'.format(_remote, _remote_path)
    print(path, remote)
    subprocess.run(['scp', path, remote])
    
def zip_videos(name):
    dir_before = os.getcwd()
    path = '{}/{}'.format(dir_before, name)
    os.chdir(path)
        
    print('Zipping images...')

    try:
        files = [_get_video_name(i) for i in range(CAM_COUNT)]
        dest = '{}_{}.zip'.format(FRIDGE_NAME, datetime.now().strftime("%Y-%m-%d-%H:%M:%S"))
        subprocess.run(['zip', '-9', dest] + files)
    except Exception:
        print("Something went wrong while zipping")
        return None
    
    return dest
    
def capture_and_send():
    capture_videos()

    _zip = zip_videos(VIDEO_PATH)

    if _zip is not None:
        send_videos(_zip)

    print('Done.')

def capture_videos():

    print('Capturing videos...')

    processes = []

    for i in [0, 2]:
        command = ['ffmpeg',
                   '-y',
                   '-i', '/dev/video{}'.format(i),
                   '-video_size', RESOLUTION,
                   '-r', str(FRAME_RATE),
                   #'--title', _get_image_name(i),
                   #'--rotate', '90',
                   #'-timestamp', datetime.now().strftime("%Y-%m-%d"),
                   '-vf',
                   "drawtext=fontfile=roboto.ttf:fontsize=36:fontcolor=yellow:text={}".format("'%{localtime}'"),
                   '-t', str(VIDEO_DURATION),
                   '{}/{}'.format(VIDEO_PATH, _get_video_name(i))
                   ]
        # oscommand = ' '.join(map(str,command))
        # os.system(oscommand)
        print(command)
        processes.append(subprocess.Popen(command))

    [process.wait() for process in processes]

if __name__ == '__main__':
    capture_and_send()


# ffmpeg -y -i /dev/video0 -video_size 648x486 -r 25 -t 10 -i /dev/video1 -video_size 648x486 -r 25 -t 10 -vf "drawtext=fontfile=roboto.ttf:fontsize=36:fontcolor=yellow:text='%{localtime}'" -map 0 test_videos/nano_video_test0.avi -vf "drawtext=fontfile=roboto.ttf:fontsize=36:fontcolor=yellow:text='%{localtime}'" -map 1 test_videos/nano_video_test1.avi