import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

led_pin = 18

GPIO.setmode(GPIO.BOARD)
GPIO.setup(led_pin, GPIO.OUT)
pwm = GPIO.PWM(led_pin, 50)
pwm.start(0)

while True:

    for i in range(100):
        pwm.ChangeDutyCycle(i)
        time.sleep(0.01)

    for i in range(100, 0, -1):
        pwm.ChangeDutyCycle(i)
        time.sleep(0.01)
