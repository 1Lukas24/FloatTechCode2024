import board
import busio

import distance
import math
import gpio as GPIO
import adafruit_pca9685
import gpsd

i2c = busio.I2C(board.SCL, board.SDA)

#Konfiguration des PCA9685
pwm = adafruit_pca9685.PCA9685()
pwm.set_pwm_freq(60)










# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(2);
