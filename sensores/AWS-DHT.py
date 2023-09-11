#import RPi.GPIO as GPIO
import Adafruit_DHT
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import sleep
from datetime import date, datetime
 
# initialize GPIO
#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BCM)
#GPIO.cleanup()
sensor = Adafruit_DHT.DHT11
pin = 4
 
# AWS IoT certificate based connection
myMQTTClient = AWSIoTMQTTClient("Reaspberryclient")
myMQTTClient.configureEndpoint("asdfasdfqewf-ats.iot.us-west-2.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/home/pi/AWS/AWSIoT/AmazonRootCA1.pem", "/home/pi/AWS/AWSIoT/private.pem.key", "/home/pi/AWS/AWSIoT/certificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
 
#connect and publish
myMQTTClient.connect()
myMQTTClient.publish("thing01/info", "connected", 0)
 
#loop and publish sensor reading
while 1:    
    now = datetime.utcnow()
    now_str = now.strftime('%Y-%m-%dT%H:%M:%SZ') #e.g. 2016-04-18T06:12:25.877Z

    humedad, temperatura = Adafruit_DHT.read_retry(sensor, pin)
    
    if humedad is not None and temperatura is not None:
        payload = 'Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity)
        print payload
        myMQTTClient.publish("thing01/data", payload, 0)
        #print(f'Temperatura={temperatura:.2f}*C  Humedad={humedad:.2f}%')
        
    else:
        print('Fallo la lectura del sensor.Intentar de nuevo')

    time.sleep(5)
    
    #now = datetime.utcnow()
    #now_str = now.strftime('%Y-%m-%dT%H:%M:%SZ') #e.g. 2016-04-18T06:12:25.877Z
    #instance = dht11.DHT11(pin = 4) #BCM GPIO04
    #result = instance.read()
    #if result.is_valid():
     #   payload = '{ "timestamp": "' + now_str + '","temperature": ' + str(result.temperature) + ',"humidity": '+ str(result.humidity) + ' }'
     #   print payload
     #   myMQTTClient.publish("thing01/data", payload, 0)
     #   sleep(4)
   # else:
    #    print (".")
     #   sleep(1)
