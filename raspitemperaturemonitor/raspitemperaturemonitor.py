"""Main module."""

import time
import adafruit_dht
import board
from sqlite3wrapper.sqlite3wrapper import DatabaseManager

dht_device = adafruit_dht.DHT22(board.D18)

while True:
    temperature = dht_device.temperature
    huminity = dht_device.humidity

    print(f"Temperature:{temperature}, Huminity:{huminity}")
    time.sleep(5)