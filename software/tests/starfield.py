import time
import serial
import random


def set_cursor(y, x):
    return bytes([0x1f, 0x40 + y, 0x40 + x])


s = serial.Serial('/dev/tty.usbserial-DVEGe11BS13',
                  baudrate=9600, parity='N', stopbits=1,  timeout=0)

t = 0

# s.write(b'\x1f\x2d')

NUM = 20

stars = []
for k in range(NUM):
    stars.append([0,0,0,0,0])

def shuffle():
    s.write(b'\x0c')
    for k in range(NUM):
        x = random.randint(-30, 30)
        y = random.randint(-30, 30)
        z = random.randint(-100, 100)
        stars[k][0] = x
        stars[k][1] = y
        stars[k][2] = z

shuffle()

x = 1
y = 1
dx = 1
dy = 1

dot1 = "."  # s% (x,y)
dot2 = "o"  # s% (x,y)
dot3 = "#"  # s% (x,y)
space = " "  # s% (x,y)

while True:
    for k in range(NUM):
        x = stars[k][3]
        y = stars[k][4]
        if x > 1 and y > 1 and x < 35 and y < 23:
            s.write(set_cursor(y, x))
            s.write(space.encode("ascii"))
        z = stars[k][2] + 110
        x = int(20 + stars[k][0] * 110 / z)
        y = int(12 + stars[k][1] * 110 / z)
        stars[k][3] = x
        stars[k][4] = y
        if x > 1 and y > 1 and x < 35 and y < 23 and z > 10:
            if z < 150:
                s.write(set_cursor(y, x))
                s.write(dot3.encode("ascii"))
            elif z < 170:
                s.write(set_cursor(y, x))
                s.write(dot2.encode("ascii"))
            else:
                s.write(set_cursor(y, x))
                s.write(dot1.encode("ascii"))

    if s.inWaiting() > 0:
        data_str = s.read()
        print(data_str)
        if len(data_str) > 0:
            shuffle()
    # res = s.read(0)
    # print(res)
    time.sleep(0.1)

    for k in range(NUM):
        stars[k][2] -= 15
        if stars[k][2] < -100:
            stars[k][2] = 100
            stars[k][0] = random.randint(-30, 30)
            stars[k][1] = random.randint(-30, 30)
