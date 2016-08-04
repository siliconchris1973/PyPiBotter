#!/usr/bin/env python3

import RPi.GPIO as GPIO # Import the GPIO Library

class GpIOSingleton:
    """ A python singleton """
    # Define GPIO pins of forward and backwards ultrasonic sensor to use on the Pi
    pinDistanceForwardsTrigger = 17
    pinDistanceForwardsEcho = 18

    pinDistanceBackwardsTrigger = 19
    pinDistanceBackwardsEcho = 20

    # Set variables for the GPIO motor pins
    pinMotorAForwards = 10
    pinMotorABackwards = 9
    pinMotorBForwards = 8
    pinMotorBBackwards = 7

    # How many times to turn the pin on and off each second
    Frequency = 20
    # How long the pin stays on each cycle, as a percent
    DutyCycleA = 30
    DutyCycleB = 30
    # Settng the duty cycle to 0 means the motors will not turn
    Stop = 0

    # Set the GPIO to software PWM at 'Frequency' Hertz
    pwmMotorAForwards = GPIO.PWM(pinMotorAForwards, Frequency)
    pwmMotorABackwards = GPIO.PWM(pinMotorABackwards, Frequency)
    pwmMotorBForwards = GPIO.PWM(pinMotorBForwards, Frequency)
    pwmMotorBBackwards = GPIO.PWM(pinMotorBBackwards, Frequency)

    def __init__(self):
        # Set the GPIO modes
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # Set pins as output and input
        GPIO.setup(self.pinDistanceForwardsTrigger, GPIO.OUT)  # Trigger
        GPIO.setup(self.pinDistanceForwardsEcho, GPIO.IN)      # Echo

        GPIO.setup(self.pinDistanceBackwardsTrigger, GPIO.OUT)  # Trigger
        GPIO.setup(self.pinDistanceBackwardsEcho, GPIO.IN)      # Echo

        # Set the GPIO Pin mode to be Output
        GPIO.setup(self.pinMotorAForwards, GPIO.OUT)
        GPIO.setup(self.pinMotorABackwards, GPIO.OUT)
        GPIO.setup(self.pinMotorBForwards, GPIO.OUT)
        GPIO.setup(self.pinMotorBBackwards, GPIO.OUT)

    def __exit__(self, exc_type, exc_val, exc_tb):
        GPIO.cleanup()

class __impl:
    """ Implementation of the singleton interface """
    def spam(self):
        """ Test method, return singleton id """
        return id(self)

    # storage for the instance reference
    __instance = None

    def __init__(self):
        """ Create singleton instance """
        # Check whether we already have an instance
        if GpIOSingleton.__instance is None:
            # Create and remember instance
            GpIOSingleton.__instance = GpIOSingleton.__impl()

        # Store instance reference as the only member in the handle
        self.__dict__['_Singleton__instance'] = GpIOSingleton.__instance

        # Start the software PWM with a duty cycle of 0 (i.e. not moving)
        __instance.pwmMotorAForwards.start(__instance.Stop)
        __instance.pwmMotorABackwards.start(__instance.Stop)
        __instance.pwmMotorBForwards.start(__instance.Stop)
        __instance.pwmMotorBBackwards.start(__instance.Stop)

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)

