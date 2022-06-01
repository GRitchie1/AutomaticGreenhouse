# AutomaticGreenhouse

## Introduction
This project is to design and build a solar powered outdoor greenhouse that can monitor and control the temperature & humidity of the air as well as automatically water the plants using collected rainwater.

The design of this project is intended to be highly modular, with the ability to chain multiple target nodes (units) together to allow for data to be combined and analysed by a single controller node.  The power supply from the solar power system will also be chained to allow for a more simple power distribution setup.

## Contents
| Topic | Description |
|-------|-------------|
| [Design](#design) | An overview of the design of the project |
| [Parts Lists](#parts-lists) | Up to date parts lists for the project |
| [PCBs](#pcbs) | Information regarding the design and manufacture of the custom printed circuit boards |

## Design
Each target node in the system will be based upon a Raspberry Pi Pico and all hardware interfacing will be done using a custom PCB.  The controller node will be a Raspberry Pi 4 managed using [Balena](https://www.balena.io/).  Communication between the target nodes and the controller node will be handled using MQTT over Ethernet.

Each node will feature space for 6 planters, and will have a modular irrigation system to allow for planters to be easily added and removed.

Each node will feature the following sensors:
- Temperature
- Air Humidity
- Soil moisture sensors (1 per planter)
- Light Level (front and back of unit)
- Water level to monitor irrigation system
- Camera (optional: adds ability to implement timelapses and machine learning)

Each node will feature the following control systems:
- Light (LED strips)
- Temperature/Humidity (DC Fan)
- Soil moisture (Water Solenoid/Pump)

An overview of the system layout can be seen below.
![System Overview](https://user-images.githubusercontent.com/55364420/171460407-145d79df-f9f1-4df8-a510-924a53a7123f.png)

## Parts Lists

**Note the following parts lists are not complete and may change.**

The following parts are required to build one node PCB.

| Part         | Qty | Description     |
|--------------|-----|-----------------|
| [Pi Pico](https://thepihut.com/products/raspberry-pi-pico)      | 1  |The microcontroller used to control the node. |
| [TCA9548A I2C Multiplexer](https://thepihut.com/products/adafruit-tca9548a-i2c-multiplexer)  | 1  | I2C multiplexer to allow connection of up to 8 soil humidity sensors with the same I2C address  |
| N-Channel Mosfet | 5 | Control outputs |

The following sensors are required to build one node.

| Sensor         | Qty | Description     |
|--------------|-----|-----------------|
| [Temperature/Humidity](https://thepihut.com/products/adafruit-sensiron-sht31-d-temperature-humidity-sensor-breakout) | 1 | Monitor air temperature and humidity in the greenhouse. |
| [Soil Humidity](https://thepihut.com/products/adafruit-stemma-soil-sensor-i2c-capacitive-moisture-sensor-ada4026) | 6 | Monitor soil humidity of each planter. |
| Light Sensor | 2 | Monitor wavelengths of light to optimise growth. |
| Water Level Switch | 1 | Monitor the stored water level to trigger an alert if it gets too low. |

## PCBs
The PCBs are designed in [EASYEDA](https://easyeda.com/) and can be ordered from [JLC PCB](https://jlcpcb.com/).

The parts for the PCBs can be found in the [Parts Lists](#parts-lists).
