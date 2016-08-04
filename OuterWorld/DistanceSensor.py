#!/usr/bin/env python3
#
# read ultrasonic distance sensor data
#
# Author:   pibotter@gmx.de
# Version:  0.0.1
# Date:     1st Aug. 2016
#
#
# This class is based on the CamJam EduKit 3 - Robotics / Worksheet 6 – Measuring Distance
# The original code alongside documentation on the hardware setup can be found on github
#

import RPi.GPIO as GPIO # Import the GPIO Library
import time
import sys

class UsDistanceSensor:

    # Define GPIO pins of forward and backwards ultrasonic sensor to use on the Pi
    pinDistanceForwardsTrigger = 17
    pinDistanceForwardsEcho = 18

    pinDistanceBackwardsTrigger = 19
    pinDistanceBackwardsEcho = 20

    fwDistances = []
    bwDistances = []

    def __init__(self):
        # Set the GPIO modes
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(True)

        # Set pins as output and input
        GPIO.setup(self.pinDistanceForwardsTrigger, GPIO.OUT)  # Trigger
        GPIO.setup(self.pinDistanceForwardsEcho, GPIO.IN)      # Echo

        GPIO.setup(self.pinDistanceBackwardsTrigger, GPIO.OUT)  # Trigger
        GPIO.setup(self.pinDistanceBackwardsEcho, GPIO.IN)      # Echo

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Reset GPIO settings
        GPIO.cleanup()

    def getAverageForwardsReading(self):
        for i in range(1, 10):
            self.getForwardsReading()
            time.sleep(0.3)

        average = sum(self.fwDistances) / len(self.fwDistances)
        return(str(average))

    def getAverageBackwardsReading(self):
        for i in range(1, 10):
            self.getBackwardsReading()
            time.sleep(0.3)

        average = sum(self.bwDistances) / len(self.bwDistances)
        return(str(average))

    def getForwardsReading(self):
        try:
            # Set trigger to False (Low)
            GPIO.output(self.pinDistanceForwardsTrigger, False)

            # Allow module to settle
            time.sleep(0.5)

            # Send 10us pulse to trigger
            GPIO.output(self.pinDistanceForwardsTrigger, True)
            time.sleep(0.00001)
            GPIO.output(self.pinDistanceForwardsTrigger, False)

            # Start the timer
            StartTime = time.time()

            # The start time is reset until the Echo pin is taken high (==1)
            while GPIO.input(self.pinDistanceForwardsEcho)==0:
                StartTime = time.time()

            # Stop when the Echo pin is no longer high - the end time
            while GPIO.input(self.pinDistanceForwardsEcho)==1:
                StopTime = time.time()
                # If the sensor is too close to an object, the Pi cannot
                # see the echo quickly enough, so we have to detect that
                # problem and say what has happened.
                if StopTime-StartTime >= 0.04:
                    #print("Hold on there!  You're too close for me to see.")
                    StopTime = StartTime
                    break

            # Calculate pulse length
            ElapsedTime = StopTime - StartTime

            # Distance pulse travelled in that time is
            # time multiplied by the speed of sound (cm/s)
            Distance = ElapsedTime * 34326

            # That was the distance there and back so halve the value
            Distance = Distance / 2

            self.fwDistances.append(Distance)

            return Distance
        except:
            GPIO.cleanup()

    def getBackwardsReading(self):
        try:
            # Set trigger to False (Low)
            GPIO.output(self.pinDistanceBackwardsTrigger, False)

            # Allow module to settle
            time.sleep(0.5)

            # Send 10us pulse to trigger
            GPIO.output(self.pinDistanceBackwardsTrigger, True)
            time.sleep(0.00001)
            GPIO.output(self.pinDistanceBackwardsTrigger, False)

            # Start the timer
            StartTime = time.time()

            # The start time is reset until the Echo pin is taken high (==1)
            while GPIO.input(self.pinDistanceBackwardsEcho)==0:
                StartTime = time.time()

            # Stop when the Echo pin is no longer high - the end time
            while GPIO.input(self.pinDistanceBackwardsEcho)==1:
                StopTime = time.time()
                # If the sensor is too close to an object, the Pi cannot
                # see the echo quickly enough, so we have to detect that
                # problem and say what has happened.
                if StopTime-StartTime >= 0.04:
                    #print("Hold on there!  You're too close for me to see.")
                    StopTime = StartTime
                    break

            # Calculate pulse length
            ElapsedTime = StopTime - StartTime

            # Distance pulse travelled in that time is
            # time multiplied by the speed of sound (cm/s)
            Distance = ElapsedTime * 34326

            # That was the distance there and back so halve the value
            Distance = Distance / 2

            self.bwDistances.append(Distance)

            return Distance
        except:
            GPIO.cleanup()

def main():
    if (len(sys.argv) > 1):
        if (sys.argv[1] == '--forward'):
            sensor = UsDistanceSensor()

            print('Starting Demo Cycle on Forward Distance Sensor')

            for i in range(1, 10):
                status = sensor.getForwardsReading()
                sensor.fwDistances.append(status)
                print(status)
                time.sleep(0.3)

            average = sum(sensor.fwDistances) / len(sensor.fwDistances)
            print('Average distance of the 10 last readings was ' + str(average))
            GPIO.cleanup()
        elif (sys.argv[1] == '--backward'):
            sensor = UsDistanceSensor()

            print('Starting Demo Cycle on Backward Distance Sensor')

            for i in range(1, 10):
                status = sensor.getBackwardsReading()
                sensor.bwDistances.append(status)
                print(status)
                time.sleep(0.3)

            average = sum(sensor.bwDistances) / len(sensor.bwDistances)
            print('Average distance of the 10 last readings was ' + str(average))
            GPIO.cleanup()
        elif (sys.argv[1] == '--both'):
            sensor = UsDistanceSensor()

            print('Starting Demo Cycle on Forward and Backward Distance Sensor')

            for i in range(1, 10):
                status = sensor.getForwardsReading()
                sensor.fwDistances.append(status)
                status = sensor.getBackwardsReading()
                sensor.bwDistances.append(status)
                time.sleep(0.3)

            average = sum(sensor.fwDistances) / len(sensor.fwDistances)
            print('Average distance of the 10 last forward readings was ' + str(average))
            average = sum(sensor.bwDistances) / len(sensor.bwDistances)
            print('Average distance of the 10 last backward readings was ' + str(average))
            GPIO.cleanup()
        else:
            print('If you want to get some readings from the forwards or backwards distance sensor \n'
                  'you may call the script with --forward or --backward or --both')
    else:
        print('Usually this script should not be run standalone. \n'
              'If you want to get some readings from the forwards or backwards distance sensor \n'
              'you may call the script with --forward or --backward or --both')

if __name__ == '__main__':
    main()
