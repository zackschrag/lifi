import RPi.GPIO as GPIO
import time
import math

GPIO.setmode(GPIO.BOARD)

activePins = [7,11,15,13]
SLEEP_DELAY = 0.04
NUMBER_OF_ITERATIONS = int(math.floor(1/SLEEP_DELAY))

print "Number of iterations: ", NUMBER_OF_ITERATIONS

for i in range(len(activePins)):
    GPIO.setup(activePins[i],GPIO.OUT)

for i in range(NUMBER_OF_ITERATIONS):
    for i in range(len(activePins)):
        time.sleep(SLEEP_DELAY)
        GPIO.output(activePins[i],True)
        time.sleep(SLEEP_DELAY)
        GPIO.output(activePins[i],False)

for i in range(len(activePins)):
    GPIO.output(activePins[i],False)
GPIO.cleanup()



