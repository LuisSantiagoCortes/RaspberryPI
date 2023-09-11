import RPi.GPIO as GPIO
import time                             #Importamos el paquete time
from w1thermsensor import W1ThermSensor,Sensor #Importamos el paquete W1ThermSensor
import Adafruit_ADS1x15 # Import the ADS1x15 module.

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import sleep
from datetime import date, datetime


            # sensores de temperatura
sensor1 = W1ThermSensor(sensor_type=Sensor.DS18B20, sensor_id="02159177b7f2") #Creamos el objeto sensor1
sensor2 = W1ThermSensor(sensor_type=Sensor.DS18B20, sensor_id="02169177d139") #Creamos el objeto sensor2
sensor3 = W1ThermSensor(sensor_type=Sensor.DS18B20, sensor_id="021891774f26") #Creamos el objeto sensor3


            # sensores de humedad
# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()
# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
GAIN = 1

# Datos para cuadrar bien los sensores de humedad
Scale_hum_Max_X = 100
Scale_hum_min_X = 0

Scale1_hum_Max_y = 26200
Scale1_hum_min_y = 7000

Scale2_hum_Max_y = 26200
Scale2_hum_min_y = 7000

Scale3_hum_Max_y = 26200
Scale3_hum_min_y = 7000


#formula de la pendiente m = (Y2 - Y1) / (X2 - X1)
Scale1_pen = (Scale1_hum_Max_y - Scale1_hum_min_y) / (Scale_hum_min_X - Scale_hum_Max_X)
Scale2_pen = (Scale2_hum_Max_y - Scale2_hum_min_y) / (Scale_hum_min_X - Scale_hum_Max_X)
Scale3_pen = (Scale3_hum_Max_y - Scale3_hum_min_y) / (Scale_hum_min_X - Scale_hum_Max_X)


            # sensores de lluvia o pluviometro
GPIO.setmode(GPIO.BCM)
Pin_pluvi = 17
GPIO.setup(Pin_pluvi, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#Agrego contadores
count = 0
Total_pluvi = 0
factor_pluvi = 0.2794
#funcion cuando se active la interrupcion
def pluviometer(channel):
    global count
    count = count + 1
#Declara pin de interrupcion, tipo de interrupcion, funcion a la que llama cuando se activa la interrupcion, tiempo
GPIO.add_event_detect(Pin_pluvi, GPIO.FALLING, callback=pluviometer, bouncetime=30)


                #Coneccion con AWS
# AWS IoT certificate based connection
myMQTTClient = AWSIoTMQTTClient("rqrergfdvdfsq")
myMQTTClient.configureEndpoint("rqfdasdfhqergbwrhy-ats.iot.us-west-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/home/pi/AWS/AWSIoT/AmazonRootCA1.pem", "/home/pi/AWS/AWSIoT/private.pem.key", "/home/pi/AWS/AWSIoT/certificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
print('Iniating IoT Core topic....')
#connect and publish
myMQTTClient.connect()

print('Connecting IoT Core topic....')

myMQTTClient.publish("thing01/info", "connected", 0)

print('publish IoT Core topic....')

while True:
    
    #Obtenemos la temperatura en centígrados
    temperature1 = sensor1.get_temperature()                
    temperature2 = sensor2.get_temperature()
    temperature3 = sensor3.get_temperature()
    
    #Obtenemos la humedad en bits
    humedity1 = adc.read_adc(0, gain=GAIN)
    humedity2 = adc.read_adc(1, gain=GAIN)
    humedity3 = adc.read_adc(2, gain=GAIN)
    #Obtenemos la humedad en %
    #formula de la ecuación de la recta (Y - Y1) = m(X - X1)
    #Y - Y1 = mX - mX1
    #Y - Y1 + mX1 = mX
    #X = (Y - Y1 + mX1)/m
    Scale1 = (humedity1 - Scale1_hum_min_y + (Scale1_pen * Scale_hum_Max_X)) / Scale1_pen
    Scale2 = (humedity2 - Scale2_hum_min_y + (Scale2_pen * Scale_hum_Max_X)) / Scale2_pen
    Scale3 = (humedity3 - Scale3_hum_min_y + (Scale3_pen * Scale_hum_Max_X)) / Scale3_pen
    
    Total_pluvi = factor_pluvi * count
    
    payfeatures = "Datos estacion metereologica | "
    paytemp = 'Temp_1 : {0:0.2f} °C | ' 'Temp_2 : {1:0.2f} °C | ' 'Temp_3 : {2:0.2f} °C | '.format(temperature1,temperature2,temperature3)
    payhum = 'hum_1 : {0:0.2f} % | ' 'hum_2 : {1:0.2f} % | ' 'hum_3 : {2:0.2f} % | '.format(Scale1,Scale2,Scale3)
    paypluvi = 'rain : {0:0.2f} %'.format(Total_pluvi)
    
    payload1 = payfeatures + paytemp + payhum + paypluvi
    
    print(payload1)
    myMQTTClient.publish("thing01/data", payload1, 0)
    
    time.sleep(2) 