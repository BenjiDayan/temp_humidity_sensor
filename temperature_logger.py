import sys
sys.path.append('/home/pi/Adafruit_CircuitPython_DHT')
import adafruit_dht as adht
import board

from datetime import datetime
import wandb
import time

# pin 11 is for some reason GPIO 17?
# this is 6 along on the bottom.
dhtDevice = adht.DHT22(board.D17)

def get_t_h():
    try:
        t = dhtDevice.temperature
    except RuntimeError:
        t = None
    time.sleep(0.01)
    try:
        h = dhtDevice.humidity
    except RuntimeError:
        h = None
    return t, h


t, h = get_t_h()
print(t, h)


run = wandb.init(
    # Set the project where this run will be logged
    project="pi_temperature_logger",
    # Track hyperparameters and run metadata
    config={
        "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

while True:
    t, h = get_t_h()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    out = {"temperature": t, "humidity": h, "time": now}
    print(out, flush=True)
    try:
        wandb.log(out)
    except Exception:
        pass
    time.sleep(5)


#### To run:
# nohup python3 temperature_logger.py >> temperature_log.txt 2>&1 &

