import RPi.GPIO as GPIO
import time

# Pin Definitons:
ledPin = 17 
butPin = 18 

# Pin Setup:
GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(butPin, GPIO.IN) 

# Initial state for LEDs:
GPIO.output(ledPin, GPIO.LOW)

print("Here we go! Press CTRL+C to exit")
try:
    while 1:
        if GPIO.input(butPin):
            GPIO.output(ledPin, GPIO.HIGH)
            time.sleep(0.075)
            GPIO.output(ledPin, GPIO.LOW)
            time.sleep(0.075)
        else:
            GPIO.output(ledPin, GPIO.HIGH)
except KeyboardInterrupt:
    GPIO.cleanup() 
