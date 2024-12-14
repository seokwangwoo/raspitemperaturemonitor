"""Main module."""

import time
import adafruit_dht
import board
from raspitemperaturemonitor.db import add_data

dht_device = adafruit_dht.DHT22(board.D18)

print("Start monitoring")

while True:
    temperature = 0
    huminity = 0
    count = 0

    for i in range(5):
        try:
            temperature += float(dht_device.temperature)
            huminity += float(dht_device.humidity)
            count += 1
        except Exception as e:
            print(e)
            continue

        time.sleep(1)

    if count == 0:
        continue

    temperature = temperature / count
    huminity = huminity / count

    with open(r"/home/seo/projects/raspitemperaturemonitor/data.csv", "w") as f:
        f.write(f"{temperature},{huminity}")

    add_data(temperature, huminity)

    print("I am running!")

dht_device.exit()
