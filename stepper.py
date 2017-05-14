#!/usr/bin/python
#--------------------------------------
#    ___  ___  _ ____          
#   / _ \/ _ \(_) __/__  __ __ 
#  / , _/ ___/ /\ \/ _ \/ // / 
# /_/|_/_/  /_/___/ .__/\_, /  
#                /_/   /___/   
#
#    Stepper Motor Test
#
# A simple script to control
# a stepper motor.
#
# Author : Matt Hawkins
# Date   : 28/09/2015
#
# http://www.raspberrypi-spy.co.uk/
#
#--------------------------------------

# Import required libraries
import sys
import time
import RPi.GPIO as GPIO

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Define GPIO signals to use
# Physical pins 11,15,16,18
# GPIO17,GPIO22,GPIO23,GPIO24
StepPins = [17,18,27,22]

WaitTime = 0.01

# Set all pins as output
for pin in StepPins:
  print "Setup pins"
  GPIO.setup(pin,GPIO.OUT)
  GPIO.output(pin, False)

# Define advanced sequence
# as shown in manufacturers datasheet
Seq = [[1,0,0,1],
       [1,0,0,0],
       [1,1,0,0],
       [0,1,0,0],
       [0,1,1,0],
       [0,0,1,0],
       [0,0,1,1],
       [0,0,0,1]]
      
pin_r = 21
pin_g = 20
GPIO.setup(pin_r,GPIO.OUT)
GPIO.setup(pin_g,GPIO.OUT)

StepCount = len(Seq)

class Engine: 
    Right = 1
    RightFast = 2
    Left = -1
    LeftFast = -2

    def padToCmd(self, val):
        tolerance = 0.3
        limit = 0.65
        if(val > tolerance and val < limit):
            cmd = self.Right
        elif(val >= limit):
            cmd = self.RightFast
        elif(val > -limit and val < -tolerance):
            cmd = self.Left
        elif(val <= -limit):
            cmd = self.LeftFast
        else:
            cmd = 0
        return cmd

    def step(self, value): 
        self.StepCounter += value
        if (self.StepCounter>=StepCount):
            self.StepCounter = 0
        if (self.StepCounter<0):
            self.StepCounter = StepCount+value

        self.sendPins()

    def sendPins(self): 
        for pin in range(0, 4):
            xpin = StepPins[pin]
            if Seq[self.StepCounter][pin]!=0:
                GPIO.output(xpin, True)
            else:
                GPIO.output(xpin, False)

    def __init__(self):
        self.StepCounter = 0

def ledsOff():
    GPIO.output(pin_r, GPIO.LOW)
    GPIO.output(pin_g, GPIO.LOW)

def greenLedOn():
    GPIO.output(pin_g, GPIO.HIGH)

def redLedOn():
    GPIO.output(pin_r, GPIO.HIGH)

engine = Engine()

def SteeringLoop(pstate):
    while True:
        cmd = engine.padToCmd(pstate["rstick"])
        if(cmd):
            print "Cmd: %d" % cmd
            engine.step(cmd)
            if(cmd > 0):
                greenLedOn()
            else:
                redLedOn()
        else:
            ledsOff()
        time.sleep(WaitTime)
