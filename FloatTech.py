#Code für das Boot VersionQ2.2024
import time
import math
import RPi.GPIO as GPIO
import Adafruit_PCA9685
import gpsd


#Globale Variablen
target_lat = 0;
target_lon = 0;
current_lat = 0;
current_lon = 0;

# GPIO Setup für Abstandssensoren
GPIO.setmode(GPIO.BCM)
TRIG_FRONT = 23
ECHO_FRONT = 24
TRIG_LEFT = 27
ECHO_LEFT = 22
TRIG_RIGHT = 5
ECHO_RIGHT = 6

GPIO.setup(TRIG_FRONT, GPIO.OUT)
GPIO.setup(ECHO_FRONT, GPIO.IN)
GPIO.setup(TRIG_LEFT, GPIO.OUT)
GPIO.setup(ECHO_LEFT, GPIO.IN)
GPIO.setup(TRIG_RIGHT, GPIO.OUT)
GPIO.setup(ECHO_RIGHT, GPIO.IN)

# Initialisierung des PCA9685
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)


# Funktion zum Setzen der Motorgeschwindigkeit. Mithilfe des PCA9685
def set_motor_speed(motor_channel, speed):
    pwm.set_pwm(motor_channel, 0, speed)


# Funktion zur Entfernungsmessung mit Ultraschallsensor
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


# Funktion zum Lesen der GPS-Koordinaten aus einer Datei. Hier wird aus der Text Datei die Koordinatel eingelesen und gespeichert
def koordinaten_einlesen(filename):
    with open(filename, 'r') as file:
        koordinaten = [line.strip() for line in file.readlines()]
    return koordinaten



#Hier wird Mithilfe von Formeln aus dem Geounterricht die Entfernung zweier GPS Punkte berechnet
def berechne_abstand_koordinate(lat1, lon1, lat2, lon2):
    R = 6371000  # Radius der Erde in Metern
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


#Hier wird etwas ähnliches wie oben gemacht, nur das wir hier die Richtung zur nächsten Koordinate kalkulieren anstatt die Entfernung
def berechnung_richtung(lat1, lon1, lat2, lon2):
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_lambda = math.radians(lon2 - lon1)
    y = math.sin(delta_lambda) * math.cos(phi2)
    x = math.cos(phi1) * math.sin(phi2) - math.sin(phi1) * math.cos(phi2) * math.cos(delta_lambda)
    richtung = (math.degrees(math.atan2(y, x)) + 360) % 360
    return richtung


#Mit dieser Funktion und den zuvor errechneten Werten, wird die Zielführung durchgeführt.
def fahren_zur_koordinate(target_lat, target_lon, current_lat, current_lon):
    abstand_koordinate = berechne_abstand_koordinate(current_lat, current_lon, target_lat, target_lon)
    if abstand_koordinate < 5:  # Ziel erreicht
        set_motor_speed(0, 0)
        set_motor_speed(1, 0)
        return True
    else:
        richtung = berechnung_richtung(current_lat, current_lon, target_lat, target_lon)
        if richtung < 180: #Hier passiert das essenzielle. Sollte der Winkel welcher zum Ziel führt über einer gewissen Grad Ziel ist wird ausgeglichen. Solte dieser fast auf perfekt sein, dann soll nichts gemacht werden
            set_motor_speed(0, 300)  # Linker Motor langsamer
            set_motor_speed(1, 400)  # Rechter Motor schneller
        elif richtung > 180:
            set_motor_speed(0, 400)  # Linker Motor schneller
            set_motor_speed(1, 300)  # Rechter Motor langsamer
        else:
            set_motor_speed(0, 400)  #
            set_motor_speed(1, 400)  # Beide Motoren gleich
        return False


# Funktion zur Hindernisvermeidung
def Autonome_Fahrt():
    abstand_vorne = abstand(TRIG_FRONT, ECHO_FRONT)
    abstand_links = abstand(TRIG_LEFT, ECHO_LEFT)
    abstand_rechts = abstand(TRIG_RIGHT, ECHO_RIGHT)
#Hier wird grundlegen die Hinerdnisserkennung und ausweichung durchgeführt
    if abstand_vorne < 100: #Sollte ein Objekt vorne zu nahe kommen, bremst das Boot ab
        print("Objekt Vorne erkannt. Weiche aus")
        set_motor_speed(0, 350)
        set_motor_speed(1, 350)
    elif abstand_links < 150: #Sollte ein Objekt links zu nah sein, weiche nach Rechts aus
        print("Objekt Links erkannt. Weiche aus")
        set_motor_speed(0, 250)
        set_motor_speed(1, 350)
    elif abstand_rechts < 150: #Sollte ein Objekt Rechts zu nah sein, weiche nahc links aus
        print("Objekt Rechts erkannt. Weiche aus")
        set_motor_speed(0, 350)
        set_motor_speed(1, 250)
    else:
        print("Weg ist frei") #Sollte nix da sein dann fahre nach der Route und gib ihm
      fahren_zur_koordinate(target_lat, target_lon, current_lat, current_lon)


if __name__ == "__main__":
    koordinaten = koordinaten_einlesen('route.txt')

    gpsd.connect()

    for koordinaten in koordinaten:
        target_lat, target_lon = map(float, koordinaten.split(','))

        while True:
            packet = gpsd.get_current()
            current_lat, current_lon = packet.lat, packet.lon

            Autonome_Fahrt()#Ausführen der Autonomen Fahrt

            time.sleep(0.1)  # Kurz warten, bevor der nächste Schritt gemacht wird

    print("Juhuuuu, ich bin angekommen. Ihr könnt mich jetzt wenn mein Ziel an Land liegt aus dem Wasser holen. Mir wird schon echt kalt langsam.")
    GPIO.cleanup()
