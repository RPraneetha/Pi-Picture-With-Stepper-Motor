# Pi-Picture-With-Stepper-Motor
Project - Takes images or videos while connected to a stepper motor

## To run

- ssh to pi
- Clone the repo 
- cd into repo
- run the stepper_pi file with arguments -r and -d, -r for number of rotations and -d for direction

## Arguments

- -r : Number of rotations
- -d : Direction 
    - cw = clockwise (upwards)
    - ccw = counter-clockwise (downwards)
    
## Config file

Many configurable parameters are present in the config file. 

The main ones to change are:
- REMOTE_ADDRESS : IP address of the machine you want to transfer the photos to
- REMOTE_PATH : Path of the remote machine
- REMOTE_USER : Username of remote machine
