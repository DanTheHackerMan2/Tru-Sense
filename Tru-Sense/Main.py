
import spidev
from time import sleep

# First open up SPI bus
spi = spidev.SpiDev()
spi.open(0,0)

# Initialize what sensor is where
lightChannel = 0
tempChannel = 1
sleepTime = 1

def getReading(channel):
    # First pull the raw data from the chip
    rawData = spi.xfer([1, (8 + channel) << 4, 0&#93;)
    # Process the raw data into something we understand.
    processedData = ((rawData&#91;1&#93;&3) << 8) + rawData&#91;2&#93;
    return processedData

def convertVoltage(bitValue, decimalPlaces=2):
    voltage = (bitValue * 3.3) / float(1023)
    voltage = round(voltage, decimalPlaces)
    return voltage

def convertTemp(bitValue, decimalPlaces=2):
    # Converts to degrees Celsius
    temperature = ((bitValue * 330)/float(1023) - 50)
    temperature = round(temperature, decimalPlaces)
    return temperature

while True:
    lightData = getReading(lightChannel)
    tempData = getReading(tempChannel)
    lightVoltage = convertVoltage(lightData)
    tempVoltage = convertVoltage(tempData)
    temperature = convertTemp(tempData)

    # Print ALL THE THINGS:
    print("Light bitValue = {} ; Voltage = {} V".format(lightData, lightVoltage))
    print("Temp bitValue = {} ; Voltage = {} V ; Temp = {} C".format(\
        tempData, tempVoltage, temperature))
    sleep(sleepTime)
#>