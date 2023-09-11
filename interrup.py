import RPi.GPIO as GPIO
import time
import os

contaA = 0
contaB = 0

ledPin = 22
#Setup
GPIO.setmode(GPIO.BCM)

GPIO.setup(ledPin,GPIO.OUT)

GPIO.setup(23,GPIO.IN)
GPIO.setup(24,GPIO.IN)

GPIO.output(ledPin,LOW)

#Callbacks
def CuentaA(channel):
    global contaA
    contaA += 1
    #os.system("clear")
    
    GPIO.output(ledPin, GPIO.LOW)
    print ("Contador A: {}".format(contaA))
    print ("Contador B: {}".format(contaB))
    
def CuentaB(channel):
    global contaB
    contaB += 1
    #os.system("clear")
    GPIO.output(ledPin, GPIO.HIGH)
    print ("Contador A: {}".format(contaA))
    print ("Contador B: {}".format(contaB))

#Interrupciones
GPIO.add_event_detect(23, GPIO.FALLING, callback = CuentaA, bouncetime=2000)
GPIO.add_event_detect(24, GPIO.FALLING, callback = CuentaB, bouncetime=2000)

#print ("Contador A: ").contaA
#print ("Contador B: ").contaB

#Bucle principal
while True:
    pass

GPIO.cleanup()
