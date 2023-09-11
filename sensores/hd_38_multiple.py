import time

# Import the ADS1x15 module.
import Adafruit_ADS1x15


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

print('Reading ADS1x15 values, press Ctrl-C to quit...')

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

while True:
    humedity1 = adc.read_adc(0, gain=GAIN)
    humedity2 = adc.read_adc(1, gain=GAIN)
    humedity3 = adc.read_adc(2, gain=GAIN)
    
    Scale1 = (humedity1 - Scale1_hum_min_y + (Scale1_pen * Scale_hum_Max_X)) / Scale1_pen
    Scale2 = (humedity2 - Scale2_hum_min_y + (Scale2_pen * Scale_hum_Max_X)) / Scale2_pen
    Scale3 = (humedity3 - Scale3_hum_min_y + (Scale3_pen * Scale_hum_Max_X)) / Scale3_pen
    
    print('humedity 1: {0}'.format(Scale1))
    print('humedity 2: {0}'.format(Scale2))
    print('humedity 3: {0}'.format(Scale3))
    
    time.sleep(1)