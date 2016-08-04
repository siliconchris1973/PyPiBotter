#!/usr/bin/env python3
#
# drive the motors of the robot
#
# Author:   pibotter@gmx.de
# Version:  0.0.1
# Date:     1st Aug. 2016
#
#
# This class is based on the CamJam EduKit 3 - Robotics / Worksheet 7 – PWM driving
# The original code alongside documentation on the hardware setup can be found on github
#

import RPi.GPIO as GPIO # Import the GPIO Library
import time
import sys

class MotorController:
    # Set variables for the GPIO motor pins
    PORT_MOTOR_A_FORWARDS = 10
    PORT_MOTOR_A_BACKWARDS = 9
    PORT_MOTOR_B_FORWARDS = 8
    PORT_MOTOR_B_BACKWARDS = 7

    # How many times to turn the pin on and off each second
    FREQUENCY = 20
    # How long the pin stays on each cycle, as a percent
    DUTY_CYCLE_A = 30
    DUTY_CYCLE_B = 30
    # Settng the duty cycle to 0 means the motors will not turn
    STOP_VALUE = 0

    def MotorController(self, port_motor_a_forwards, port_motor_a_backwards,
                        port_motor_b_forwards, port_motor_b_backwards,
                        frequency, duty_cycle_a, duty_cycle_b, stop_value):
        self.PORT_MOTOR_A_FORWARDS = port_motor_a_forwards
        self.PORT_MOTOR_B_FORWARDS = port_motor_b_forwards
        self.PORT_MOTOR_A_BACKWARDS = port_motor_a_backwards
        self.PORT_MOTOR_B_BACKWARDS = port_motor_b_backwards
        self.FREQUENCY = frequency
        self.DUTY_CYCLE_A = duty_cycle_a
        self.DUTY_CYCLE_B = duty_cycle_b
        self.STOP_VALUE = stop_value

    def __init__(self):
        # Set the GPIO modes
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # Set the GPIO Pin mode to be Output
        GPIO.setup(self.PORT_MOTOR_A_FORWARDS, GPIO.OUT)
        GPIO.setup(self.PORT_MOTOR_A_BACKWARDS, GPIO.OUT)
        GPIO.setup(self.PORT_MOTOR_B_FORWARDS, GPIO.OUT)
        GPIO.setup(self.PORT_MOTOR_B_BACKWARDS, GPIO.OUT)

        # Set the GPIO to software PWM at 'Frequency' Hertz
        self.pwmMotorAForwards = GPIO.PWM(self.PORT_MOTOR_A_FORWARDS, self.FREQUENCY)
        self.pwmMotorABackwards = GPIO.PWM(self.PORT_MOTOR_A_BACKWARDS, self.FREQUENCY)
        self.pwmMotorBForwards = GPIO.PWM(self.PORT_MOTOR_B_FORWARDS, self.FREQUENCY)
        self.pwmMotorBBackwards = GPIO.PWM(self.PORT_MOTOR_B_BACKWARDS, self.FREQUENCY)

        # Start the software PWM with a duty cycle of 0 (i.e. not moving)
        self.pwmMotorAForwards.start(self.STOP_VALUE)
        self.pwmMotorABackwards.start(self.STOP_VALUE)
        self.pwmMotorBForwards.start(self.STOP_VALUE)
        self.pwmMotorBBackwards.start(self.STOP_VALUE)

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Reset GPIO settings
        GPIO.cleanup()

    def setFrequency(self, frequency):
        self.FREQUENCY = frequency

    def setDutyCycleA(self, dutyCycle):
        self.DUTY_CYCLE_A = dutyCycle

    def setDutyCycleB(self, dutyCycle):
        self.DUTY_CYCLE_B = dutyCycle

    # Turn all motors off
    def stopMotors(self):
        self.pwmMotorAForwards.ChangeDutyCycle(self.STOP_VALUE)
        self.pwmMotorABackwards.ChangeDutyCycle(self.STOP_VALUE)
        self.pwmMotorBForwards.ChangeDutyCycle(self.STOP_VALUE)
        self.pwmMotorBBackwards.ChangeDutyCycle(self.STOP_VALUE)
        return 'Stopping (Motors A & B off)'

    # Turn motor A off
    def stopMotorA(self):
        self.pwmMotorAForwards.ChangeDutyCycle(self.STOP_VALUE)
        self.pwmMotorABackwards.ChangeDutyCycle(self.STOP_VALUE)
        return 'Motor A off'

    # Turn motor B off
    def stopMotorB(self):
        self.pwmMotorBForwards.ChangeDutyCycle(self.STOP_VALUE)
        self.pwmMotorBBackwards.ChangeDutyCycle(self.STOP_VALUE)
        return 'Motor B off'

    # Turn both motors forwards
    def driveForwards(self):
        self.pwmMotorAForwards.ChangeDutyCycle(self.DUTY_CYCLE_A)
        self.pwmMotorABackwards.ChangeDutyCycle(self.STOP_VALUE)
        self.pwmMotorBForwards.ChangeDutyCycle(self.DUTY_CYCLE_B)
        self.pwmMotorBBackwards.ChangeDutyCycle(self.STOP_VALUE)
        return 'Driving forwards (Motors A & B forward)'

    # Turn both motors backwards
    def driveBackwards(self):
        self.pwmMotorAForwards.ChangeDutyCycle(self.STOP_VALUE)
        self.pwmMotorABackwards.ChangeDutyCycle(self.DUTY_CYCLE_A)
        self.pwmMotorBForwards.ChangeDutyCycle(self.STOP_VALUE)
        self.pwmMotorBBackwards.ChangeDutyCycle(self.DUTY_CYCLE_B)
        return 'Driving backwards (Motors A & B backward)'

    # Turn left
    def turnLeft(self):
        self.pwmMotorAForwards.ChangeDutyCycle(self.STOP_VALUE)
        self.pwmMotorABackwards.ChangeDutyCycle(self.DUTY_CYCLE_A)
        self.pwmMotorBForwards.ChangeDutyCycle(self.DUTY_CYCLE_B)
        self.pwmMotorBBackwards.ChangeDutyCycle(self.STOP_VALUE)
        return 'Turning left (Motor A backward & B forward)'

    # Turn Right
    def turnRight(self):
        self.pwmMotorAForwards.ChangeDutyCycle(self.DUTY_CYCLE_A)
        self.pwmMotorABackwards.ChangeDutyCycle(self.STOP_VALUE)
        self.pwmMotorBForwards.ChangeDutyCycle(self.STOP_VALUE)
        self.pwmMotorBBackwards.ChangeDutyCycle(self.DUTY_CYCLE_B)
        return 'Turning right (Motor A forward & B backward)'


def main():
    if (len(sys.argv) > 1):
        if (sys.argv[1] == '--demo'):
            motor = MotorController()
            print('Starting Demo Cycle')
            status = motor.driveForwards()
            print(status)
            time.sleep(0.5)
            status = motor.turnLeft()
            print(status)
            time.sleep(0.5)
            status = motor.driveBackwards()
            print(status)
            time.sleep(0.5)
            status = motor.turnRight()
            print(status)
            time.sleep(0.5)
        else:
            print('If you want to test the motor controller start the script with --demo')
    else:
        print('Usually this script should not be run standalone. \n'
              'If you want to test the motor controller start the script with --demo')

if __name__ == '__main__':
    main()
