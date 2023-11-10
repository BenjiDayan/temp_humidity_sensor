import time
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas
from PIL import Image, ImageFont

##### Get temp and humidity from logfile
from datetime import datetime
import subprocess


def get_message():
    output = subprocess.check_output(['tail', '-n', '10', 'temperature_log.txt']).decode()
    # e.g.
    # ...
    # {'temperature': 22.4, 'humidity': 59.1, 'time': '2023-11-10 15:03:30'}
    # {'temperature': 22.4, 'humidity': 62.3, 'time': '2023-11-10 15:03:36'}
    # {'temperature': None, 'humidity': 62.3, 'time': '2023-11-10 15:03:41'}
    datadict = {'temperature': None, 'humidity': None, 'time': None}
    # read lines in reverse order, update with latest value
    for line in output.split('\n')[::-1]:
        try:
            foo = eval(line)
        except Exception as e:
            foo = {}
        if type(foo) is not dict:
            continue
        for key, val in foo.items():
            if key in datadict and datadict[key] == None:
                datadict[key] = val

    time_obj = datetime.strptime(datadict['time'], '%Y-%m-%d %H:%M:%S')
    datadict['time'] = time_obj

    dd = datadict

    temp = dd['temperature']
    hum = dd['humidity']
    time = dd['time']
    time = time.strftime('%d/%m %H:%M')
    temp = str(temp) + ' ℃' if temp is not None else 'N/A ℃'
    hum = str(hum) + '%' if hum is not None else 'N/A %'
    return f'{temp} {hum}\n{time}'



# NB ssd1306 devices are monochromatic; a pixel is enabled with
#    white and disabled with black.
# NB the ssd1306 class has no way of knowing the device resolution/size.
device = ssd1306(i2c(port=1, address=0x3c), width=128, height=64, rotate=0)

# set the contrast to minimum.
device.contrast(1)

# load the rpi logo.
logo = Image.open('rpi-logo.png')

# Benji: I think we need to do rgb -> rgba
logo = logo.convert('RGBA')

# show some info.
print(f'device size {device.size}')
print(f'device mode {device.mode}')
print(f'logo size {logo.size}')
print(f'logo mode {logo.mode}')

# NB this will only send the data to the display after this "with" block is complete.
# NB the draw variable is-a PIL.ImageDraw.Draw (https://pillow.readthedocs.io/en/3.1.x/reference/ImageDraw.html).
# see https://github.com/rm-hull/luma.core/blob/master/luma/core/render.py



# # Now draw is https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html
# with canvas(device, dither=True) as draw:
#     draw.rectangle(device.bounding_box, outline='white', fill='black')
#     # We draw the logo in the top left
#     # draw.bitmap((0, 0), logo)
#     # Then we put the text in on the right side, middle height.
#     message = 'Heyo'

#     # Let's get the message from thingy
#     message = get_str(datadict)
#     message = message + '\n0'

#     fnt = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 17)
#     text_size = draw.textsize(message, font=fnt)
#     # -2 because border?
#     # draw.text((device.width - text_size[0]-2, (device.height - text_size[1]) // 2), message, fill='white', font=fnt)

#     draw.text((2, (device.height - text_size[1]) // 2), message, fill='white', font=fnt)


# # NB the display will be turn off after we exit this application.
# time.sleep(5)


def draw_msg(message):
    # Now draw is https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html
    with canvas(device, dither=True) as draw:
        draw.rectangle(device.bounding_box, outline='white', fill='black')

        fnt = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 17)
        text_size = draw.textsize(message, font=fnt)

        draw.text((2, (device.height - text_size[1]) // 2), message, fill='white', font=fnt)

for i in range(5):
    message = get_message()
    message = message + f'\n{i}'
    draw_msg(message)
    time.sleep(5)

# NB the display will be turn off after we exit this application.
time.sleep(5)