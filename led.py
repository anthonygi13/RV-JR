# Author: Giraudo Anthony, Kari Hichma, MacDonald Kilian, Marinho Louise                      
# 22 janvier 2018
# led.py

import RPi.GPIO as GPIO
import time


def clignoter_led(duree, periode, pin):
    """
    Pour une led rouge il faut une resistance de 434 ohm (si tension de la led est 2V, à verifier)
    :param duree: duree du clignotement
    :param periode: temps d'un allumage et d'une extinction
    :param pin: prendre une pin gpio, la 11 par exemple
    :return:
    """
    GPIO.setmode(GPIO.BOARD) #indique la numerotation à utiliser
    GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
    for i in range(int(duree/periode)):
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(periode/2)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(periode/2)
    GPIO.output(pin, GPIO.LOW)
    GPIO.cleanup()

def luminosite_led():
    #ça marche pas le input dans le simulateur ça arrete l'envoie du signal (a tester sur la raspberry pi)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(12, GPIO.OUT, initial=GPIO.LOW)
    pwm = GPIO.PWM(12, 200)
    pwm.start(0)
    rapport = float(input("Luminosité ? "))
    while 0.0 <= rapport and rapport <= 100.0:
        pwm.ChangeDutyCycle(rapport)
        rapport = float(input("Luminosité ? "))
    pwm.stop()
    GPIO.cleanup()