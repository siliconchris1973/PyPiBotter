#!/usr/bin/env python3
#
# Author:   pibotter@gmx.de
# Version:  0.0.1
# Date:     1st Aug. 2016
#
from flask import Flask

import sys
import logging
from logging.handlers import RotatingFileHandler

from OuterWorld import DistanceSensor as Distance
from OuterWorld import MotorController as Motor

# to change the display implementation you only need to change the import here.
from OuterWorld import Nokia5110 as Display
#from OuterWorld import DummyDisplay as Display

app = Flask(__name__)

fwSensor = Distance.UsDistanceSensor()
bwSensor = Distance.UsDistanceSensor()
driver = Motor.MotorController()
display = Display.Display()

@app.route('/')
def index():
    return app.send_static_file('templates/index.html')

@app.route('/distance/forward')
def getForwardSensor():
    fwAvgDistance = fwSensor.getAverageForwardsReading()
    fwDistance = fwSensor.getForwardsReading()

    displayStatus = display.displayText(0,0,'fw dist: ' + str(fwAvgDistance))
    app.logger.debug('fw distance avg last 10 seconds: ' + str(fwAvgDistance) + ' / now: ' + str(fwDistance))
    return 'fw distance avg last 10 seconds: ' + str(fwAvgDistance) + ' / now: ' + str(fwDistance)

@app.route('/distance/backward')
def getBackwardSensor():
    bwAvgDistance = bwSensor.getAverageBackwardsReading()
    bwDistance = bwSensor.getBackwardsReading()

    displayStatus = display.displayText(0,2,'bw dist: ' + str(bwAvgDistance))
    app.logger.debug('fw distance avg last 10 seconds: ' + str(bwAvgDistance) + ' / now: ' + str(bwDistance))
    return 'fw distance avg last 10 seconds: ' + str(bwAvgDistance) + ' / now: ' + str(bwDistance)

@app.route('/drive/stopall')
def stopMotors():
    motorStatus = driver.stopMotors()

    displayStatus = display.displayText(0,0,motorStatus)
    app.logger.debug('display status: ' + displayStatus + ' / motor status: ' + motorStatus)
    return motorStatus

@app.route('/drive/stop/a')
def stopMotorA():
    motorStatus = driver.stopMotorA()

    displayStatus = display.displayText(0,0,motorStatus)
    app.logger.debug('display status: ' + displayStatus + ' / motor status: ' + motorStatus)
    return motorStatus

@app.route('/drive/stop/b')
def stopMotorB():
    motorStatus = driver.stopMotorB()

    displayStatus = display.displayText(0,0,motorStatus)
    app.logger.debug('display status: ' + displayStatus + ' / motor status: ' + motorStatus)
    return motorStatus

@app.route('/drive/forwards')
def driveForwards():
    motorStatus = driver.driveForwards()

    displayStatus = display.displayText(0,0,motorStatus)
    app.logger.debug('display status: ' + displayStatus + ' / motor status: ' + motorStatus)
    return motorStatus

@app.route('/drive/backwards')
def driveBackwards():
    motorStatus = driver.driveBackwards()

    displayStatus = display.displayText(0,0,motorStatus)
    app.logger.debug('display status: ' + displayStatus + ' / motor status: ' + motorStatus)
    return motorStatus

@app.route('/drive/left')
def turnLeft():
    motorStatus = driver.turnLeft()

    displayStatus = display.displayText(0,0,motorStatus)
    app.logger.debug('display status: ' + displayStatus + ' / motor status: ' + motorStatus)
    return motorStatus

@app.route('/drive/right')
def turnRight():
    motorStatus = driver.turnRight()

    displayStatus = display.displayText(0,0,motorStatus)
    app.logger.debug('display status: ' + displayStatus + ' / motor status: ' + motorStatus)
    return motorStatus



def main():
    handler = RotatingFileHandler('/var/tmp/PyPiBotter.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)

    appDebug=False

    if (len(sys.argv) > 1):
        if (sys.argv[1] == '--server'):
            pass
        elif (sys.argv[1] == '--debug'):
            appDebug = True
        else:
            print('running all in console mode - please use --server to start a background server')
    else:
        print('running all in console mode and with debugging on - please use --server to start a background server')
        appDebug = True

    app.run(host='0.0.0.0', debug=appDebug)
    app.logger.info('Try the forwards and backwards sensors at /distance/forward and /distance/backward')


if __name__ == '__main__':
    main()