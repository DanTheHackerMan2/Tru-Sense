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

user_uuid= uuid.uuid4() #user uuid generation. would be set in a config file for a set in stone use
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)
channel0 = AnalogIn(mcp, MCP.P0)
channel1 = AnalogIn(mcp, MCP.P1)


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
        "FirstName": {
            "name": "Mortimer"
        },
        "MiddleName": {
            "name": "'Morty'"
        },
        "LastName": {
            "name": "Smith"
        },
        "Gender": {
            "name": "Male"
        },
        "PhoneNumber": {
            "name": "(302)831-2792"
        },
        "AlternatePhoneNumber": {
            "name": ""
        }
    }

loc_data = {
        "Street1": {
           "name": "139 The Green"
        },
        "Street2": {
           "name": ""
        },
        "City": {
            "name":"Newark"
        },
        "State": {
            "name": "DE"
        },
        "Zipcode": {
            "name": "19716"
        },
        "Fire Alarm Location": {
            "name": "Kitchen"
        }
    }

db.child("Customers").child(user_uuid).child("Contact Information").set(pers_data,user['idToken']) 
db.child("Customers").child(user_uuid).child("Location").set(loc_data,user['idToken']) 

#Set Up 
gas_con = False
gas_r = channel0.value 
temp_con = False
temp_r = channel1.value 
sensor_check=0

while True:
    if(sensor_check>=100 or sensor_check== 0):
        if(gas_r != 0 ):
            gas_con=True
        if(temp_r != 0):
            gas_con=True
        sens_Data = {
            "Gas Sensor": {
                "name": gas_con
            },
            "Temp Sensor": {
                "name": temp_con
            }
        }   
        if(sensor_check==0):
            db.child("Customers").child(user_uuid).child("Sensors Active").set(sens_Data,user['idToken'])
        db.child("Customers").child(user_uuid).child("Sensors Active").update(sens_Data,user['idToken'])
        sensor_check=1
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    gas_r = channel0.value
    temp_r = channel0.value

    print('Raw Gas ADC Value: ', gas_r)
    print('Mod Gas ADC Value: ', (gas_r-1601))

    print('Raw Temp ADC Value: ', temp_r)
    print('ADC Voltage: ' + str(channel1.voltage) + 'V')

    data = {
        "Gas": {
            "name": (channel0.value-1601)
        }
    }
    db.child("Customers").child(user_uuid).child("Readings").child(current_time).set(data,user['idToken'])
    sensor_check+=1
    time.sleep(5.0)#Limited to 20k samples a day, 85 k a seconds in a day. avg to 5