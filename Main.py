import pyrebase
from datetime import datetime
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
import time
import RPi.GPIO as GPIO
from adafruit_mcp3xxx.analog_in import AnalogIn

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)
channel = AnalogIn(mcp, MCP.P0)



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


while True:
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print('Raw ADC Value: ', channel.value)
    print('Raw ADC Value: ', (channel.value-1601))
    print('ADC Voltage: ' + str(channel.voltage) + 'V')
    data = {
        "Temp": {
            "name": "Mortimer 'Morty' Smith"
        },
        "Gas": {
            "name": (channel.value-1601)
        }
    }
    db.child("customers").child("Devices").child(current_time).set(data,user['idToken'])
    time.sleep(5.0)#Limited to 20k samples a day, 85 k a seconds in a day. avg to 5