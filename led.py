import RPi.GPIO as GPIO
import time
import math
from morse import encodeToMorse
from morse import decodeMorse


#def flashMorse(message, GPIO):
#    morse = encodeToMorse(message)
    
    
GPIO.setmode(GPIO.BOARD)

activePins = [7, 11, 13, 15]
SLEEP_DELAY = 0.5
NUMBER_OF_ITERATIONS = 200#int(math.floor(1/SLEEP_DELAY))

testCode = ".... . .-.. .-.. --- / -.. .- .. .-.. -.-- / .--. .-. --- --. .-. .- -- -- . .-. / --. --- --- -.. / .-.. ..- -.-. -.- / --- -. / - .... . / -.-. .... .- .-.. .-.. . -. --. . ... / - --- -.. .- -.-- "
print decodeMorse(testCode)

print "Number of iterations: ", NUMBER_OF_ITERATIONS

message = "Hi Matt"
for i in range(len(activePins)):
    GPIO.setup(activePins[i],GPIO.OUT)

ctr = 0

flashLength = 0
flash = False
morse = encodeToMorse(message)
print morse
#while (ctr != NUMBER_OF_ITERATIONS):
while (ctr < len(morse)):
    if (morse[ctr] == '.'):
        flashLength = 0.1
        #flashLength = 0.05
        flash = True
    elif (morse[ctr] == '-'):
        flashLength = 0.5
        #flashLength = 0.1
        flash = True
    elif (morse[ctr] == ' '):
        flashLength = 1
        flash = True
    elif (morse[ctr] == '/'):
        flashLength = 0.3
        flash = True

    if (flash):
        for i in range(len(activePins)):
            GPIO.output(activePins[i],True)

    #print "before sleep"
    time.sleep(flashLength)
    #print "after sleep"
    
    for i in range(len(activePins)):
        GPIO.output(activePins[i],False)

    time.sleep(SLEEP_DELAY)
        #time.sleep(SLEEP_DELAY)
        #if (ctr % 2 == 0):
        #    GPIO.output(activePins[i],True)
        #else:
        #    GPIO.output(activePins[i],False)
        #time.sleep(SLEEP_DELAY)
        #GPIO.output(activePins[i],True)
    #time.sleep(SLEEP_DELAY)
    ctr=ctr+1

for i in range(len(activePins)):
    GPIO.output(activePins[i],False)
GPIO.cleanup()





