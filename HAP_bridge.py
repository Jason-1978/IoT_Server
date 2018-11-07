"""An example of how to setup and start an Accessory.

This is:
1. Create the Accessory object you want.
2. Add it to an AccessoryDriver, which will advertise it on the local network,
    setup a server to answer client queries, etc.
"""
import logging
import signal

from pyhap.accessory import Bridge
from pyhap.accessory_driver import AccessoryDriver
import pyhap.loader as loader

# The below package can be found in the HAP-python github repo under accessories/
from accessories.LightBulb import LightBulb
from accessories.TemperatureSensor import TemperatureSensor


logging.basicConfig(level=logging.INFO)

LedPin1 = 12
LedPin2 = 16
TempPin = 18


def get_bridge(driver):
    """Call this method to get a Bridge instead of a standalone accessory."""
    bridge = Bridge(driver, 'Bridge')
    light_1 = LightBulb(driver, 'Red Light', pin=LedPin1)
    light_2 = LightBulb(driver, 'Blue Light', pin=LedPin2)
    bridge.add_accessory(light_1)
    bridge.add_accessory(light_2)
    temp = TemperatureSensor(driver, 'Temperature Humidity', pin=TempPin)
    bridge.add_accessory(temp)

    return bridge


def get_accessory(driver):
    """Call this method to get a standalone Accessory."""
    return LightBulb(driver, 'My Light Bulb')


# Start the accessory on port 51826
driver = AccessoryDriver(port=51826)

# Change `get_accessory` to `get_bridge` if you want to run a Bridge.
driver.add_accessory(accessory=get_bridge(driver))

# We want SIGTERM (kill) to be handled by the driver itself,
# so that it can gracefully stop the accessory, server and advertising.
signal.signal(signal.SIGTERM, driver.signal_handler)

# Start it!
driver.start()
