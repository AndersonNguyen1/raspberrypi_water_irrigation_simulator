import datetime
from cimis import run_query, retrieve_cimis_station_info, write_output_file, run_cimis
import threading
import RPi.GPIO
import math
import sys
import _thread
import relay
import I2CLCD1602
import DHT11
import SenseLED
import variable
from time import sleep

def smain():
   appKey = '130dcac4-4f8d-46ad-adf6-5579c1c54e5b'
   sites = [75]
   sites = [str(i) for i in sites]
   
   ItemInterval = 'hourly'
   start = '2019-06-13'
   end = datetime.datetime.now().strftime("%Y-%m-%d")
   station_info = retrieve_cimis_station_info()
   pulled_site_names = [station_info[x] for x in sites]
   
   
   df = run_cimis(appKey, sites, start, end, ItemInterval)
   
  
   return pulled_site_names, df
    
def Calc_ETo(avgtmp,avghum):
    
    appKey = '130dcac4-4f8d-46ad-adf6-5579c1c54e5b'
    sites = [75]
    sites = [str(i) for i in sites]
   
    interval = 'hourly'
    start = '2019-06-13'
    end = datetime.datetime.now().strftime("%Y-%m-%d")
    
    param  = 'HlyEto'
    param2 = 'HlyAirTmp'
    param3 = 'HlyRelHum'
    
    ETo = []
    EToD = []
    AirTemp = []
    AirTempD = []
    RelHum = []
    RelHumD = []
    
#    param1  = 'DayPrecip'
    
    #get the data as a list of data frames; one dataframe for each site
    site_names, cimis_data = run_query(appKey, sites, interval,
                                       start=start, end=end)
    
    
    #plot some some data and do some analysis
    params = cimis_data[0].columns.tolist()
    error_message = "{} was not in the list of available paramters. \
        Choose a parameter from the available paramters: {} \
        and try again.".format(param, params)
    #summarize the data
    if param in params:
        data = cimis_data[0][param]
        
        for date,value in data.items():
            ETo.append(value)
            EToD.append(date)
        for i in range(len(data)):
            if math.isnan(ETo[i]):
                print("prev ETo: ", ETo[i-1])
                updatedETo = ETo[i-1]
                print("prev ETo time: ", EToD[i-1])
                ETotime = EToD[i-1]
                print("nan time: ", EToD[i])
                etonantime = EToD[i]
                break
            
            #else:
                #print("same ETo")

        print('{} statistics for the period:\n{}'.format(param,
              data.describe()))
    #        data.plot(marker='o', label=data.name, legend=True)
    
    if param2 in params:
        data = cimis_data[0][param2]
        
        for date,value in data.items():
            AirTemp.append(value)
            AirTempD.append(date)
        for i in range(len(data)):
            if math.isnan(AirTemp[i]):
                print("prev AirTemp: ", AirTemp[i-1])
                updatedAirTemp = AirTemp[i-1]
                print("prev AirTemp time: ", AirTempD[i-1])
#                AirTemptime = AirTempD[i-1]
                print("nan time: ", AirTempD[i])
#                airtempnantime = AirTempD[i]
                break
            
            #else:
            #    print()
            #    #print("same AirTemp")

        print('{} statistics for the period:\n{}'.format(param2,
              data.describe()))
        
    if param3 in params:
        data = cimis_data[0][param3]
        
        for date,value in data.items():
            RelHum.append(value)
            RelHumD.append(date)
        for i in range(len(data)):
            if math.isnan(RelHum[i]):
                print("prev RelHum: ", RelHum[i-1])
                updatedRelHum = RelHum[i-1]
                print("prev RelHum time: ", RelHumD[i-1])
#                RelHumtime = RelHumD[i-1]
                print("nan time: ", RelHumD[i])
#                relhumnantime = RelHumD[i]
                break
            
            #else:
                #print("same RelHum")

        print('{} statistics for the period:\n{}'.format(param3,
              data.describe()))
    
     
    else:
        print(error_message)
        
    
    if (ETotime == etonantime):
        return(0)
    else:
        print("updatedETo, avgtmp, updatedAirTemp, updatedRelHum, avghum : ",updatedETo,avgtmp,updatedAirTemp,updatedRelHum,avghum )
        LocalETo = updatedETo*(avgtmp/updatedAirTemp)*(updatedRelHum/avghum)
        variable.Temp = updatedAirTemp
        variable.Humidity = updatedRelHum
        variable.localETO = updatedETo
    


    
    return LocalETo

def set_timer():
    Humid = [0,0,0]
    Temp = [0,0,0]

    # calculate time
    while True:
        for x in range(3):
            DHT11.loop()    #run in separate thread, and for loop
            Humid[x] = variable.Humidity
            Temp[x] = variable.Temp
            variable.localETO[x] = Calc_ETo(Temp[x],Humid[x])
            if x < 2:
                sleep(60)           #sleep for an hour  

        #add 3 last eto's, then divide by volume of water, then divide by efficiency
        variable.timer = ((variable.localETO[0]+variable.localETO[1]+variable.localETO[2])/1020)/.75
        #reset for another iteration
        Humid = [0,0,0]
        Temp = [0,0,0]
        sleep (60)

def generate_cimis():
    #file = open("CIMIS_query_hourly.xlsx", "x")
    xls_path = 'CIMIS_query_example_hourly.xlsx'
    site_names,cimis_data  = smain()
    print(site_names)
    print(cimis_data)
    #write_output_file(xls_path, cimis_data, site_names)


if __name__ == "__main__":
    generate_cimis()
    try:
        DHT11.loop()    #run in separate thread, and for loop
        _thread.start_new_thread(I2CLCD1602.setup, (0,))
        _thread.start_new_thread(SenseLED.setup, ())
        _thread.start_new_thread(relay.setup, ())
    except (KeyboardInterrupt):
            SenseLED.destroy()
            relay.destroy()
            I2CLCD1602.destroy()
            GPIO.setwarning(False)
            GPIO.cleanup()
            exit()
            
    #generate_cimis()
    
    #avgtmp = getdht.tmp()
    #avghum = getdht.hum()
    
    #LocETo = Calc_ETo(avgtmp,avghum)
    
    #print("Local ETo: ", LocETo)
    
    #Im not sure if this is right, but i did a for loop so
    # that every hour for 24 hrs it will regenerate the cimis file 
    # to get any updated values. I commented it out for now while
    # other code is still being written
    
#    for i in range(23):
#       timer = threading.Timer(3600.0, generate_cimis) 
#       timer.start() 
       
       
       
       
       
       
       
       
       
       
    
