import gpio as GPIO
import time

#GPIO Ports der distance Sensoren
TRIG_FRONT = 23
ECHO_FRONT = 24
TRIG_LEFT = 27
ECHO_LEFT = 22
TRIG_RIGHT = 5
ECHO_RIGHt = 6
#Jenachdem wie viele wir im College noch haben, eventuell rüsten wir auf noch mehr auf(Zwei Pro Seite)

#GPIO Setup
GPIO.setup(TRIG_FRONT, GPIO.OUT)
GPIO.setup(ECHO_FRONT, GPIO.IN)
GPIO.setup(TRIG_LEFT, GPIO.OUT)
GPIO.setup(ECHO_LEFT, GPIO.IN)
GPIO.setup(TRIG_RIGHT, GPIO.OUT)
GPIO.setup(ECHO_LEFT, GPIO.IN)

def abstand(trigger, echo):
    GPIO.output(trigger, True)
    time.sleep(0.00001)
    GPIO.output(trigger, False)
    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(echo) == 0:
        start_time = time.time()

    while GPIO.input(echo) == 1:
        stop_time = time.time()

    elapsed_time = stop_time - start_time
    distance = (elapsed_time * 34300) / 2
    return distance



