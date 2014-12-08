import RPi.GPIO as GPIO
import time
import math
import sys
from morse import encodeToMorse
from morse import decodeMorse
from led import LIFIClient

class LIFIServer:
    timeout = time.time() + 10
    rawMsg = ""
    morseMsg = ""
    message = ""

    rawToMorse = {
        "-" : ".",
        "--" : ".",
        "---" : "-",
        "----" : "-",
        "-----" : "-",
        "------" : " ",
        "-------" : " ",
        "--------" : " ",
        "---------" : " ",
        "----------" : "/",
        "-----------" : "/",
        }

    def convertRawToMorse(self, msg):
        charBuffer = msg.split()
        morseBuffer = ""
        for i in range(len(charBuffer)):
            morseBuffer += self.rawToMorse[charBuffer[i]]
        return morseBuffer

    def convertRawToReal(self, msg):
        morse = self.convertRawToMorse(msg)
        return decodeMorse(morse)
            
    def lightOn(self, channel):
        curr = ""

        self.timeout = time.time() + 0.5
        while (GPIO.input(channel) == GPIO.HIGH):
            curr += "-"
            time.sleep(0.01)

        curr += " "
        self.rawMsg += curr


    def readMessage(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18, GPIO.IN)

        GPIO.add_event_detect(18, GPIO.RISING, callback=self.lightOn)

        while (True):
            if (time.time() > self.timeout):
                break

        print self.convertRawToReal(self.rawMsg)
        try:
            sys.stdout.close()
        except:
            pass
        try:
            sys.stderr.close()
        except:
            pass

        GPIO.cleanup()
