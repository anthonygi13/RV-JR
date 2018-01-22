# Author: Giraudo Anthony                     
# 22 janvier 2018
# led.py

import RPi.GPIO as GPIO
import time


def clignoter_led(duree, periode, pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
    for i in range(int(duree/periode)):
        GPIO.output(pin, not GPIO.input(pin))
        time.sleep(periode)
    GPIO.cleanup()


def luminosité_led():
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