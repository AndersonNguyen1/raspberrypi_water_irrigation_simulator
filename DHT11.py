import RPi.GPIO as GPIO
import time
import Freenove_DHT as DHT
from main import Calc_ETo
import variable

DHTPin = 11     #define the pin of DHT11

def loop():
    DHTPin = 11
    dht = DHT.DHT(DHTPin)   #create a DHT class object
    sumCnt = 0              #number of reading times
    flag = 1
    while(flag == 1):
    #while(True):
        sumCnt += 1         #counting number of reading times
        chk = dht.readDHT11()     #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
        print ("The sumCnt is : %d, \t chk    : %d"%(sumCnt,chk))
        if (chk is dht.DHTLIB_OK):      #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
            flag = 0
            #Runs until valid temperature is acquired
            variable.Temp = dht.temperature
            variable.Humidity = dht.humidity
            #Temp = dht.temperature
            #Humidity = dht.humidity
            print("DHT11,OK!")
            print("Humidity : %.2f, \t Temperature : %.2f \n"%(variable.Humidity,variable.Temp))
            variable.LocalETO = Calc_ETo(variable.Temp, variable.Humidity)
            
        else:               #other errors
            print("Trying again ...")
        time.sleep(2)
'''    
if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        loop()
    except KeyboardInterrupt:
        #GPIO.cleanup()
        exit()
        '''
