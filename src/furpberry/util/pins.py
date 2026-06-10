from enum import Enum

import RPi.GPIO as GPIO

# Declare the GPIO settings
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


class Pin(Enum):
    """GPIO pin ID from Pi pin ID"""

    PI3 = 2
    PI5 = 7
    PI7 = 4
    PI8 = 14
    PI10 = 15
    PI11 = 17
    PI12 = 18
    PI13 = 27
    PI15 = 22
    PI16 = 23
    PI18 = 24
    PI19 = 10
    PI21 = 9
    PI22 = 25
    PI23 = 11
    PI24 = 8
    PI26 = 7
    PI27 = 0
    PI28 = 1
    PI29 = 5
    PI31 = 6
    PI32 = 12
    PI33 = 13
    PI35 = 19
    PI36 = 16
    PI37 = 26
    PI38 = 20
    PI40 = 21
    CS0 = 0
    CS1 = 1
