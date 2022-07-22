import time
import board
import adafruit_sht31d
import busio
import adafruit_veml7700
import adafruit_tca9548a
from adafruit_seesaw.seesaw import Seesaw

i2c = busio.I2C(board.GP17, board.GP16)    # Pi Pico RP2040

tempHumid = adafruit_sht31d.SHT31D(i2c)
veml7700 = adafruit_veml7700.VEML7700(i2c)

#Soil Sensors
tca = adafruit_tca9548a.TCA9548A(i2c)
ss0 = Seesaw(tca[0], addr=0x36)
ss1 = Seesaw(tca[1], addr=0x36)
ss2 = Seesaw(tca[2], addr=0x36)

loopcount = 0
while True:
    print("\nTemperature: %0.1f C" % tempHumid.temperature)
    print("Humidity: %0.1f %%" % tempHumid.relative_humidity)
    print("Ambient light:", veml7700.light)

    touch0 = ss0.moisture_read()
    temp0 = ss0.get_temp()
    print("temp: " + str(temp0) + "  moisture: " + str(touch0))

    touch1 = ss1.moisture_read()
    temp1 = ss1.get_temp()
    print("temp: " + str(temp1) + "  moisture: " + str(touch1))

    touch2 = ss2.moisture_read()
    temp2 = ss2.get_temp()
    print("temp: " + str(temp2) + "  moisture: " + str(touch2))

    loopcount += 1
    time.sleep(2)
    # every 10 passes turn on the heater for 1 second
    if loopcount == 10:
        loopcount = 0
        tempHumid.heater = True
        print("Sensor Heater status =", tempHumid.heater)
        time.sleep(1)
        tempHumid.heater = False
        print("Sensor Heater status =", tempHumid.heater)

