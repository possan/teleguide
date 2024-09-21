import time
import serial
import random

def set_cursor(y, x):
    return bytes([0x1f, 0x40 + y, 0x40 + x])

s = serial.Serial('/dev/tty.usbserial-DVEGe11BS13', 9600, 8, 'N', 1)

t = 0

s.write(b'\x1f\x2d')
s.write(b'\x0c')

x = 1
y = 1
dx = 1
dy = 1

while True:
    # res = s.read()
    # print(res)

    # y = int(random.randint(1,17))
    # s.write(set_cursor(y, 0))
    s.write(set_cursor(y, x))
    # s.write(b'\x0c')

    text = "boll" # s% (x,y)
    s.write(text.encode("ascii"))

    time.sleep(0.1)
    # s.write(set_cursor(3,3))

    s.write(set_cursor(y, x))
    text = "    "
    s.write(text.encode("ascii"))

    # text = "apor" # % t
    # s.write(text.encode("ascii"))

    # time.sleep(0.01)
    # t += 1

    x += dx
    y += dy
    if x > 30:
        dx = -1
        x = 31
    if y > 20:
        dy = -1
        y = 20
    if x < 1:
        dx = 1
        x = 1
    if y < 1:
        dy = 1
        y = 1
