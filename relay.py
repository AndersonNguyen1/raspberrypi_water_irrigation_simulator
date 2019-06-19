import RPi.GPIO as GPIO
import sys
import time
from time import sleep
import variable         #globals

relayPin = 13    # define the relayPin
debounceTime = 50

def setup():
    print ('Program is starting...')
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    GPIO.setup(relayPin, GPIO.OUT)   # Set relayPin's mode is output
    loop()

def loop():
    relayState = False
    lastChangeTime = round(time.time()*1000)
    reading = GPIO.HIGH

    #might have it be called in eto function too, needs include 1 min timer too    
    while (variable.motionFlag == 0):   
        if ((round(time.time()*1000) - lastChangeTime) > debounceTime):
            while True:
                sleep(10)    
                relayState = not relayState
                if relayState:
                    print("Turn off relay ...")
                else:
                    print("Turn on relay ... ")
                GPIO.output(relayPin,relayState)
           
def destroy():
    GPIO.output(relayPin, GPIO.HIGH)     # relay off
    #GPIO.cleanup()                     # Release resource
    #exit()
'''
if __name__ == '__main__':     # Program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt:  
        destroy()
        '''
