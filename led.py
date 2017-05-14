import RPi.GPIO as GPIO
import time
import sys

if len(sys.argv)>1:
    WaitTime = int(sys.argv[1])/float(1000)
else:
    WaitTime = 10/float(1000)

pin_r = 21
pin_g = 20

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pin_r,GPIO.OUT)
GPIO.setup(pin_g,GPIO.OUT)

for i in range(1000):
    print "LED red on for " + str(i)
    GPIO.output(pin_r,GPIO.HIGH)
    time.sleep(WaitTime)
    print "LED red off"
    GPIO.output(pin_r,GPIO.LOW)
    time.sleep(WaitTime)
    print "LED green on for " + str(i)
    GPIO.output(pin_g,GPIO.HIGH)
    time.sleep(WaitTime)
    print "LED green off"
    GPIO.output(pin_g,GPIO.LOW)
    time.sleep(WaitTime)


