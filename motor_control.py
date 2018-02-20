# Author: Giraudo Anthony, Marinho Louise
# 20 février 2018
# motor_control.py

import RPi.GPIO as GPIO

def controle_moteur(v_g, v_d):
    """
    :param v_g: en pourcentage (de 0 a 100)
    :param v_d: en pourcentage (de 0 a 100)
    :return:
    """

    GPIO.setmode(GPIO.BOARD)

