import RPi.GPIO as GPIO
import time
import math
import sys
from morse import encodeToMorse
from morse import decodeMorse

class LIFIClient:  
    activePins = [7, 11, 13, 15]
    SLEEP_DELAY = 0.05

    def sendMessage(self, message):
        GPIO.setmode(GPIO.BOARD)
            
        for i in range(len(self.activePins)):
            GPIO.setup(self.activePins[i],GPIO.OUT)

        ctr = 0

        flashLength = 0
        flash = False
        morse = encodeToMorse(message)

        while (ctr < len(morse)):
            if (morse[ctr] == '.'):
                flashLength = 0.02
                flash = True
            elif (morse[ctr] == '-'):
                flashLength = 0.05
                flash = True
            elif (morse[ctr] == ' '):
                flashLength = 0.08
                flash = True
            elif (morse[ctr] == '/'):
                flashLength = 0.11
                flash = True

            if (flash):
                for i in range(len(self.activePins)):
                    GPIO.output(self.activePins[i],True)

            time.sleep(flashLength)
            
            for i in range(len(self.activePins)):
                GPIO.output(self.activePins[i],False)

            time.sleep(self.SLEEP_DELAY)
            ctr=ctr+1

        for i in range(len(self.activePins)):
            GPIO.output(self.activePins[i],False)
        GPIO.cleanup()

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

        #print "hello?"
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

        #print "?"
        print self.convertRawToReal(self.rawMsg)
        self.rawMsg = ""
        self.timeout = time.time() + 15
        GPIO.remove_event_detect(18)
        try:
            sys.stderr.close()
        except:
            pass

        GPIO.cleanup()

if __name__ == "__main__":
    server = LIFIServer()
    client = LIFIClient()
    
    if (len(sys.argv) > 1):
        #while (True):
            print "Listening..."
            server.readMessage()
            m = raw_input("Enter a message: ")
            client.sendMessage(m)
            print "Listening..."
            server.readMessage()
            #sys.stdout.flush()
            #print "Waiting for message..."
            #server.readMessage()

    else:
        #while (True):
            m = raw_input("Enter a message: ")
            client.sendMessage(m)
            print "Waiting for message..."
            server.readMessage()
            m = raw_input("Enter a message: ")
            client.sendMessage(m)
            #message = raw_input("Enter a message: ")
            #client.sendMessage(message)

