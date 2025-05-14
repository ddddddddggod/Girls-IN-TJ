import RPi.GPIO as GPIO
import time

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

try:
    # Pulse delay
    while True:
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

        # Waterpump on
        if distance > 6: 
            GPIO.output(A1A, GPIO.HIGH)
        else:
            GPIO.output(A1A, GPIO.LOW)

except KeyboardInterrupt:
    GPIO.cleanup()
