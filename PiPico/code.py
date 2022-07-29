import time
import board
import adafruit_sht31d
import busio
import digitalio
import json
import adafruit_veml7700
import adafruit_tca9548a
from adafruit_seesaw.seesaw import Seesaw

#Setup
deviceID = "AutoGH_1"
control = {
            'minSoilHumid':500,
            'maxAirHumid':70
            }


### MQTT ###
from adafruit_wiznet5k.adafruit_wiznet5k import *
import adafruit_wiznet5k.adafruit_wiznet5k_socket as socket
import adafruit_minimqtt.adafruit_minimqtt as MQTT

#Ethernet
##SPI0
SPI0_SCK = board.GP18
SPI0_TX = board.GP19
SPI0_RX = board.GP16
SPI0_CSn = board.GP17


##reset
W5x00_RSTn = board.GP20

pubTopic = 'AutoGH/data'
subTopic = 'AutoGH/control'
mqtt_client = MQTT.MQTT(
    broker="192.168.1.109",  #setup your PC IP address.
    username="iotdash",
    password="iotdash",
    is_ssl=False,
    socket_pool=None,
    ssl_context=None,
    keep_alive=60,
)

def recieveMessage(client, topic, newControl):
    global control
    newControl = json.loads(newControl)
    if newControl != control:
        control = newControl

MY_MAC = (0x00, 0x01, 0x02, 0x03, 0x04, 0x05)
IP_ADDRESS = (192, 168, 1, 100)
SUBNET_MASK = (255, 255, 255, 0)
GATEWAY_ADDRESS = (192, 168, 1, 1)
DNS_SERVER = (8, 8, 8, 8)

ethernetRst = digitalio.DigitalInOut(W5x00_RSTn)
ethernetRst.direction = digitalio.Direction.OUTPUT

cs = digitalio.DigitalInOut(SPI0_CSn)

spi_bus = busio.SPI(SPI0_SCK, MOSI=SPI0_TX, MISO=SPI0_RX)

ethernetRst.value = False
time.sleep(1)
ethernetRst.value = True

eth = WIZNET5K(spi_bus, cs, is_dhcp=True, mac=MY_MAC, debug=False)

print("Chip Version:", eth.chip)
print("MAC Address:", [hex(i) for i in eth.mac_address])
print("My IP address is:", eth.pretty_ip(eth.ip_address))

MQTT.set_socket(socket, eth)

mqtt_client.on_message = recieveMessage

print("Connecting to Broker...")
mqtt_client.connect()

### Sensors ###
i2c = busio.I2C(board.GP5, board.GP4)    #Init I2C

tempHumid = adafruit_sht31d.SHT31D(i2c)
veml7700 = adafruit_veml7700.VEML7700(i2c)

#Soil Sensors
tca = adafruit_tca9548a.TCA9548A(i2c)
numSoilSensors = 3
soilSensors=[Seesaw(tca[i], addr=0x36) for i in range(numSoilSensors)]

### Outputs ###
#Water Pump
pump = digitalio.DigitalInOut(board.GP2)
pump.direction = digitalio.Direction.OUTPUT

#Water Pump
fan = digitalio.DigitalInOut(board.GP3)
fan.direction = digitalio.Direction.OUTPUT

#Vars
loopcount = 0

while True:
    mqtt_client.loop()
    mqtt_client.subscribe(subTopic)
    loopcount += 1

    obj={}
    obj['ID'] = deviceID
    obj['control']=control

    #Env Sensors
    obj['temp'] = tempHumid.temperature
    obj['humid'] = tempHumid.relative_humidity
    obj['light'] = veml7700.light

    #Read Soil Sensors
    soilData = []
    totalSoilHumid = 0
    for sensor in soilSensors:
        soilObj = {}
        soilObj['soilMoisture'] = sensor.moisture_read()
        soilObj['soilTemp'] = sensor.get_temp()
        soilData.append(soilObj)
        totalSoilHumid += soilObj['soilMoisture']
    avgSoilHumid = totalSoilHumid/numSoilSensors
    obj['soil'] = soilData

    #Control outputs
    if avgSoilHumid < control['minSoilHumid']:
        pump.value = True
    else:
        pump.value = False

    if obj['humid'] > control['maxAirHumid']:
        fan.value = True
    else:
        fan.value = False

    #Output States
    obj['pump'] = int(pump.value)
    obj['fan'] = int(fan.value)

    packet = json.dumps(obj)
    mqtt_client.publish(pubTopic, packet)



    time.sleep(1)

    # every 20 passes turn on the heater for 1 second
    if loopcount >= 20 or tempHumid.heater == True:
        if tempHumid.heater == True:
            tempHumid.heater = False
        else:
            loopcount = 0
            tempHumid.heater = True

print("Disconnecting from %s" % mqtt_client.broker)
mqtt_client.disconnect()
