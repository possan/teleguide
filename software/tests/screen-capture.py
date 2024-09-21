from PIL import Image
from mss import mss
import time
import serial
import random


sct = mss()

def set_cursor(y, x):
    return bytes([0x1f, 0x40 + y, 0x40 + x])

def normal_size():
    return b'\x8c'

def double_height():
    return b'\x8d'

def double_width():
    return b'\x8e'

s = serial.Serial('/dev/tty.usbserial-DVEGe11BS13',
                  baudrate=9600, parity='N', stopbits=1,  timeout=0)

t = 0


s.write(b'\x0c')
# s.write(b'\x1f\x2d')

# s.write(double_width())
# s.write(double_height())

NUM = 20

x = 1
y = 1
dx = 1
dy = 1

# dot1 = "/"  # s% (x,y)
# dot2 = "\\"  # s% (x,y)
CHARS = [' ', ' ', '.', ':', '8', '#']

r = 0

while True:
    if r == 0:
        mon = {"top": 400,  "left": 400, "width": 512, "height": 384}
        pic = sct.grab(mon)
        img = Image.new("RGB", pic.size)
        pixels = zip(pic.raw[2::4], pic.raw[1::4], pic.raw[::4])
        img.putdata(list(pixels))
        img = img.resize((40, 25))
        img = img.convert(mode='L', dither=True)
        pixels = img.load()

    rowpixels = [int(pixels[c, r] * 6 / 256) for c in range(0, 40, 1)]
    rowchars = ''.join([CHARS[b] for b in rowpixels])
    print (rowchars)
    s.write(set_cursor(r + 1, 1))
    s.write(rowchars.encode("ascii"))

    r += 1
    if r > 20:
        r = 0

    if s.inWaiting() > 0:
        data_str = s.read()
        print(data_str)

    time.sleep(0.05)
