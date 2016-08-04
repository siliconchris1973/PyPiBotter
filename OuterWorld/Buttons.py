#!/usr/bin/env python3
#
# retrieve and act on buttons pressed
#
# Author:   pibotter@gmx.de
# Version:  0.0.1
# Date:     1st Aug. 2016
#
import sys
import time
import os
import RPi.GPIO as GPIO


PIN_SHUTDOWN_BUTTON = 40

# Use the Broadcom SOC Pin numbers
# Setup the Pin with Internal pullups enabled and PIN in reading mode.
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_SHUTDOWN_BUTTON, GPIO.IN, pull_up_down = GPIO.PUD_UP)


# Our function on what to do when the button is pressed
def Shutdown(channel, appDebug):
    if (appDebug == True):
        print('shutdown pressed')
    else:
        os.system("sudo shutdown -h now")

def main():
    if (len(sys.argv) > 1):
        if (sys.argv[1] == '--server'):
            pass
        elif (sys.argv[1] == '--debug'):
            print('running all in console mode - please use --server to start a background server')
            appDebug = True
        else:
            print('running all in console mode - please use --server to start a background server')
            appDebug = True
    else:
        print('running all in console mode and with debugging on - please use --server to start a background server')
        appDebug = True

    # Add our function to execute when the button pressed event happens
    GPIO.add_event_detect(PIN_SHUTDOWN_BUTTON, GPIO.FALLING, callback = Shutdown, bouncetime = 2000)

    # Now wait!
    while 1:
        time.sleep(1)

if __name__ == '__main__':
    main()