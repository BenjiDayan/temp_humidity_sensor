import adafruit_dht as adht
import board

# pin 11 is for some reason GPIO 17?
# this is 6 along on the bottom.
dhtDevice = adht.DHT22(board.D17)

t = dhtDevice.temperature
h = dhtDevice.humidity
print(t, h)
