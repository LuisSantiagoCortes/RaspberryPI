import time
import serial

ser = serial.Serial(
        port='/dev/ttyS0',
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)

print ("Starting program")

while 1:
    if ser.inWaiting() > 0:
        x=ser.readline().decode('ascii')
        print (x)
