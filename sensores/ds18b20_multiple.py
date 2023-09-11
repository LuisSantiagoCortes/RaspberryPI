import time                             #Importamos el paquete time
from w1thermsensor import W1ThermSensor ,Sensor #Importamos el paquete W1ThermSensor

#sensor1 = W1ThermSensor(sensor_type=Sensor.DS18B20, sensor_id="02159177b7f2") #Creamos el objeto sensor1
sensor2 = W1ThermSensor(sensor_type=Sensor.DS18B20, sensor_id="02169177d139") #Creamos el objeto sensor2
sensor3 = W1ThermSensor(sensor_type=Sensor.DS18B20, sensor_id="021891774f26") #Creamos el objeto sensor3

while True:
#    temperature1 = sensor1.get_temperature()                #Obtenemos la temperatura en centígrados
    temperature2 = sensor2.get_temperature()
    temperature3 = sensor3.get_temperature() 
    print( # "Temperature_1 is %s celsius" % temperature1) #,
          "Temperature_2 is %s celsius" % temperature2,
          "Temperature_3 is %s celsius" % temperature3)  #Imprimimos el resultado
    time.sleep(1) 
