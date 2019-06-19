import RPi.GPIO as GPIO
import I2CLCD1602
import variable

detection_flag = 1

ledPin = 16
sensorPin = 32

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(ledPin,GPIO.OUT)
    GPIO.setup(sensorPin, GPIO.IN)
    loop()
    
def loop():
    while True:
        if GPIO.input(sensorPin) == GPIO.HIGH:
            #When movement is detected, stop irrigating
            #Also display LCD that movement was detected
            
            variable.motionFlag = detection_flag  #update global
            
            GPIO.output(ledPin, GPIO.HIGH)
            #detection_flag = 1
            I2CLCD1602.setup(detection_flag)
            #print('led on...')
        else:
            GPIO.output(ledPin,GPIO.LOW)
            #print('led off...')

            variable.motionFlag = not detection_flag  #update global

            
def destroy():
    #GPIO.cleanup()
    exit()

'''
if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
        '''
