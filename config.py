CAM_COUNT = 4
IMAGE_PATH = 'PictureWithStepperMotor/test_images'
VIDEO_PATH = 'test_videos'
VIDEO_DURATION = 15 #In Seconds
RESOLUTION = '1280x720'
FRIDGE_NAME = 'MARK-III'
REMOTE_ADDRESS = '10.4.10.55'
# '192.168.178.76'
REMOTE_PATH = '/Users/rammy/fridge-images'
REMOTE_USER = 'rammy'
IMAGES_THRESHOLD = 1.3
CLOSED_THRESHOLD = 2.8
LOG_PATH = 'logs/camservice.log'
LOG_FORMAT = '{' \
             '"@timestamp": "%(asctime)s", ' \
             '"@version": "1", ' \
             '"message": "%(message)s", ' \
             '"logger_name": "%(name)s", ' \
             '"level": "%(levelname)s"' \
             '}'
FRAME_RATE = 25