import RPi.GPIO as GPIO
import time
import math
import sys
from morse import encodeToMorse
from morse import decodeMorse

class LIFIClient:  
    activePins = [7]
    SLEEP_DELAY = 0.01

    def sendMessage(self, message):
        GPIO.setmode(GPIO.BOARD)
            
        for i in range(len(self.activePins)):
            GPIO.setup(self.activePins[i],GPIO.OUT)

        ctr = 0

        flashLength = 0
        morse = encodeToMorse(message)

        while (ctr < len(morse)):
            if (morse[ctr] == '.'):
                flashLength = 0.02
            elif (morse[ctr] == '-'):
                flashLength = 0.05
            elif (morse[ctr] == ' '):
                flashLength = 0.08
            elif (morse[ctr] == '/'):
                flashLength = 0.11

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
    MESSAGE_WAIT = 300
    timeout = time.time() + MESSAGE_WAIT
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

        realMsg = self.convertRawToReal(self.rawMsg)
        if (realMsg == "EXIT"):
            print "Connection closed by peer"
            try:
                sys.stderr.close()
            except:
                pass

            GPIO.cleanup()
            exit()
        print realMsg
        self.rawMsg = ""
        self.timeout = time.time() + self.MESSAGE_WAIT
        GPIO.remove_event_detect(18)
        try:
            sys.stderr.close()
        except:
            pass

        GPIO.cleanup()

if __name__ == "__main__":
    server = LIFIServer()
    client = LIFIClient()

    print "To close the program, type 'exit' when prompted to enter a message"
    if (len(sys.argv) > 1):
        while (True):
            print "Listening..."
            server.readMessage()
            m = raw_input("Enter a message: ")
            if (m == "exit"):
                client.sendMessage(m)
                exit()
            client.sendMessage(m)

    else:
        while (True):
            m = raw_input("Enter a message: ")
            if (m == "exit"):
                client.sendMessage(m)
                exit()
            client.sendMessage(m)
            print "Waiting for message..."
            server.readMessage()

