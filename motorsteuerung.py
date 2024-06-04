import gpio
import adafruit_pca9685 as PCA9685
import busio
import board
import time

#Initialisierung des I2C Bus
i2c = busio.I2C(board.SCL, board.SDA)


#Konfiguration des PCA9685
pca = PCA9685(i2c)
pcafrequency = 60

#ESC Auflisten

def ESCGeschwindigkeitsetzen(esc, speed):

def vollefahrtvoraus():

