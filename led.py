import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
#GPIO.setup(36,GPIO.OUT)

for i in range(50):
    GPIO.output(15,True)
    GPIO.output(11,True)
    GPIO.output(7,False)
    GPIO.output(13,False)
    time.sleep(0.08)
    GPIO.output(15,False)
    GPIO.output(11,False)
    GPIO.output(7,True)
    GPIO.output(13,True)
    time.sleep(0.08)

GPIO.output(15,False)
GPIO.output(11,False)
GPIO.output(7,False)
GPIO.output(13,False)
GPIO.cleanup()



