import RPi.GPIO as GPIO
import time

contador = 0
GPIO.setmode(GPIO.BCM)
pluvipin = 17
GPIO.setup(pluvipin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
preci = 0

pfactor = 0.2794

def pluviometro(channel):
    global contador
    contador = contador + 1
    
GPIO.add_event_detect(pluvipin, GPIO.FALLING, callback=pluviometro, bouncetime=30)

while True:
    
    preci = pfactor*contador
    print("precipitacion(1/m2): {}".format(preci))
    time.sleep(1)
    print("---------------------------")