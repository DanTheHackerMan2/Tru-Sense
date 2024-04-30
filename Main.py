import pyrebase
from datetime import datetime
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
import time
import RPi.GPIO as GPIO
from adafruit_mcp3xxx.analog_in import AnalogIn
import uuid
import time
from bmp280 import BMP280
try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

user_uuid= "c5382c3a-61eb-4133-b0dc-e188ff3553c4" #uuid.uuid4() #user uuid generation. would be set in a config file for a set in stone use
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)
channel0 = AnalogIn(mcp, MCP.P0)


#Config stuff
config = {
  "apiKey": "AIzaSyCyMG6PX4A3KTnd7DBrvOf-0Gxit0ESYBs",
  "authDomain": "tru-sense-c272e.firebaseapp.com",
  "databaseURL": "https://tru-sense-c272e-default-rtdb.firebaseio.com/",
  "storageBucket": "tru-sense-c272e.appspot.com",
  "messagingSenderId": "711985614594",
  "appId": "1:711985614594:web:53d7283df8283ae0effc1b",
  #"measurementId": "",
  "projectId":"tru-sense-c272e"
}

firebase= pyrebase.initialize_app(config)
db = firebase.database()
auth = firebase.auth()
user = auth.sign_in_with_email_and_password("dstahovich@outlook.com", "Jordan53")
user = auth.refresh(user['refreshToken'])

pers_data = {
        "FirstName": "Mortimer",
        "MiddleName": "Morty",
        "LastName": "Smith",
        "Gender":  "Male",
        "PhoneNumber": "(302)831-2792",
        "AlternatePhoneNumber": ""
    }

loc_data = {
        "Street1": "139 The Green", 
        "Street2": "",
        "City": "Newark",
        "State": "DE",
        "Zipcode": "19716",
    }

db.child("Customers").child(user_uuid).child("Contact_Information").set(pers_data,user['idToken']) 
db.child("Customers").child(user_uuid).child("Location").set(loc_data,user['idToken']) 
#
current_list = db.child("Customers").child(user_uuid).child("Devices").get().val() or []
    # Update the entire list in the database
db.child("Customers").child(user_uuid).child("Devices").set(current_list)
#Set Up
dev_loc="Kitchen"
devLoc={
    "DeviceLocation": dev_loc
}
db.child("Customers").child(user_uuid).child("Devices").child(0).set(devLoc,user['idToken'])
gas_con = False
gas_r = channel0.value 
bus = SMBus(1)
bmp280_1 = BMP280(0x77)
temp_con = False
temp_r = BMP280.get_temperature(bmp280_1)
sensor_check=0
Warning=False
WarningArray=[0,0,0,0,0]
print(WarningArray)
rNum=0
while True:
    current_list = db.child("Customers").child(user_uuid).child("Devices").child(0).child("Readings").get().val() or []
    if(sensor_check>=100 or sensor_check== 0):
        if(gas_r != 0 ):
            gas_con=True
        if(temp_r != 0):
            gas_con=True
        sens_Data = {
            "GasSensor": gas_con,
            "TempSensor": temp_con
        }   
        if(sensor_check==0):
            db.child("Customers").child(user_uuid).child("Devices").child(0).child("SensorsActive").set(sens_Data,user['idToken'])
        else:
            db.child("Customers").child(user_uuid).child("Devices").child(0).child("SensorsActive").update(sens_Data,user['idToken'])
        sensor_check=1

    gas_r = channel0.value
    temp_r = BMP280.get_temperature(bmp280_1)

    print('Raw Gas ADC Value: ', gas_r)
    print('Mod Gas ADC Value: ', (gas_r-1601))
    print('Raw Temp ADC Value: ', temp_r)
    print('ADC Voltage: ' + str(channel0.voltage) + 'V')

        # Define a dictionary with the data you want to add, including a timestamp
    data_to_add = {
        "ReadingNum":rNum,
        "Gas": gas_r,
        "Temp": temp_r,
        "Timestamp": datetime.now().strftime("%H:%M:%S")
    }

    # Append the new data to the current list
    current_list.append(data_to_add)
    # Update the entire list in the database
    db.child("Customers").child(user_uuid).child("Devices").child(0).child("Readings").set(current_list)
    #History

    WarningArray[0]=WarningArray[1]
    WarningArray[1]=WarningArray[2]
    WarningArray[2]=WarningArray[3]
    WarningArray[3]=WarningArray[4]
    WarningArray[4]=data_to_add
    if(gas_r>1000): #warning threshold
        #Save warning data to db
        #set warning varible to true
        Warning=True;    
    warn_Data = {
        "IsWarning": Warning,
        "Warning1": WarningArray[0],
        "Warning2": WarningArray[1],
        "Warning3": WarningArray[2],
        "Warning4": WarningArray[3],
        "Warning5": WarningArray[4]
    }
    db.child("Customers").child(user_uuid).child("Devices").child(0).child("Warning").set(warn_Data)
    sensor_check+=1
    rNum+=1
    time.sleep(5.0)#Limited to 20k samples a day, 85 k a seconds in a day. avg to 5



#gpio 18 for led on board
#gpio 13 for speaker
#was these before board was changed
