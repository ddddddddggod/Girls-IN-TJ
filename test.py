import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)

TRIG = 18
ECHO = 21

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, False)
print("Starting.....")
time.sleep(2)

while True:
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
      pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
      pulse_stop = time.time()

    pulse_time = pulse_stop - pulse_start

    distance = pulse_time * 17150
    print(round(distance, 2))

    time.sleep(1)

    if distance < 4:
        print("Water will overflow")
    
    else:
        GPIO.output(4, False)
