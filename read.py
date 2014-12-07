import RPi.GPIO as GPIO
import time
import math
import sys
from morse import encodeToMorse
from morse import decodeMorse

def swapValue(curr):
    if (curr == GPIO.LOW):
        curr = GPIO.HIGH
    if (curr == GPIO.HIGH):
        curr = GPIO.LOW
    return curr

def convertToBits(curr):
    if (curr == GPIO.LOW):
        return 0
    if (curr == GPIO.HIGH):
        return 1

def convertRawToMorse(msg):
    print msg
    charBuffer = msg.split()
    morseBuffer = ""
    for i in range(len(charBuffer)):
        if (charBuffer[i] == "-"):
            morseBuffer = morseBuffer + "."
        elif (charBuffer[i] == "---"):
            morseBuffer = morseBuffer + "-"
        elif(charBuffer[i] == "-----"):
            morseBuffer = morseBuffer + " "
        else:
            morseBuffer = morseBuffer + "/"
    return morseBuffer

def convertRawToReal(msg):
    msg = convertRawToMorse(msg)
    return decodeMorse(msg)
        
def lightOn(channel):
    global timeout
    global rawMsg
    timeout = time.time() + 2
    while (GPIO.input(channel) == GPIO.HIGH):
        rawMsg = rawMsg + "-"
        time.sleep(0.2)
    rawMsg = rawMsg + " "
    #print rawMsg
    #print convertRawToReal(rawMsg)

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN)

GPIO.add_event_detect(18, GPIO.RISING, callback=lightOn, bouncetime=200)

timeout = time.time() + 10
rawMsg = ""
morseMsg = ""
message = ""
while (True):
    if (time.time() > timeout):
        break

#print rawMsg
#morseMsg = convertRawToMorse(rawMsg)
#print morseMsg
print convertRawToReal(rawMsg)
GPIO.cleanup()
