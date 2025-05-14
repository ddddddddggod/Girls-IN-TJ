# 사진 5초마다 촬영 후 저장
from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO
import time
import cv2
import sys
import numpy as np
import matplotlib.pyplot as plt
import math

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

TRIG = 18
ECHO = 21

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Ultrasonic Output Reset
GPIO.output(TRIG, False)
time.sleep(2)

A1A = 4
GPIO.setup(A1A, GPIO.OUT)
GPIO.output(A1A, GPIO.LOW)

# Camera
camera = PiCamera()

for i in range(5):
    sleep(5)
    camera.capture('/home/pi/image.jpg'.format(i))

# 저장한 jpg 파일 읽고 평균값 추출
src = cv2.imread('/home/pi/image.jpg'.format(i))

if src is None:
    print('Image load failed!')
    sys.exit()

colors = ['b', 'g', 'r']
bgr_planes = cv2.split(src)

for (p, c) in zip(bgr_planes, colors):
    hist = cv2.calcHist([p], [0], None, [256], [0, 256])

Red = []
Green = []
Blue = []

for x in src:
    for y in x:
        Red.append(y[0])
        Green.append(y[1])
        Blue.append(y[2])

R_max = max(Red)
G_max = max(Green)
B_max = max(Blue)

R_avg = sum(Red) / len(Red)
G_avg = sum(Green) / len(Green)
B_avg = sum(Blue) / len(Blue)

print("Max Value")
print("R : ", R_max)
print("G : ", G_max)
print("B : ", B_max)

print("Avg Value")
print("R : ", R_avg)
print("G : ", G_avg)
print("B : ", B_avg)


cv2.imshow('src', src)
cv2.waitKey(1)

# Camera_water_pump
relay = 13
GPIO.setup(relay, GPIO.OUT)
GPIO.output(relay, GPIO.LOW)

start = time.time()
end = time.time()
duration = start - end

try:
    while True:
        # Ultrasonic_Pulse_delay
        pulse_start = 0
        pulse_stop = 0
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        while GPIO.input(ECHO) == 0:
            pulse_start = time.time()

        while GPIO.input(ECHO) == 1:
            pulse_stop = time.time()

        pulse_time = pulse_stop - pulse_start

        distance = pulse_time * 17150

        time.sleep(1)
        # Ultrasonic_water_pump_on
        if distance > 6:
            GPIO.output(A1A, GPIO.HIGH)
        else:
            GPIO.output(A1A, GPIO.LOW)
        # Camera_water_pump_on
        if R_avg > 100:
            GPIO.output(relay, GPIO.HIGH)
            if duration == 5:
                sys.exit()
        else:
            GPIO.output(relay, GPIO.LOW)

except KeyboardInterrupt:
    GPIO.cleanup()
