# Author: Giraudo Anthony, Marinho Louise
# 20 février 2018
# motor_control.py

import RPi.GPIO as GPIO


def controle_moteur(vitesse_gauche, vitesse_droite, inverser_sens_moteur_gauche=False, inverser_sens_moteur_droit=False):
    """
    :param v_g: en pourcentage (de -100 a 100)
    :param v_d: en pourcentage (de -100 a 100)
    :return:
    A gauche
    B droite
    "-" correspond au sens "arriere"
    """
    if inverser_sens_moteur_gauche:
        vitesse_gauche = -vitesse_gauche
    if inverser_sens_moteur_droit:
        vitesse_droite = -vitesse_droite

    ENA = 16
    ENB = 18
    IN1 = 29
    IN2 = 31
    IN3 = 33
    IN4 = 35

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(ENA, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(ENB, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(IN2, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(IN3, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(IN4, GPIO.OUT, initial=GPIO.LOW)

    pwm_A = GPIO.PWM(ENA, 50)  # frequence a determiner
    pwm_B = GPIO.PWM(ENB, 50)

    if vitesse_gauche > 0:
        GPIO.output(IN1, GPIO.HIGH)  # rotation sens horaire
        GPIO.output(IN2, GPIO.LOW)
        pwm_A.start(abs(vitesse_gauche))
    elif vitesse_gauche < 0:
        GPIO.output(IN1, GPIO.LOW) # anti horaire
        GPIO.output(IN2, GPIO.HIGH)
        pwm_A.start(abs(vitesse_gauche))

    if vitesse_droite > 0:
        GPIO.output(IN3, GPIO.HIGH)  # rotation sens horaire
        GPIO.output(IN4, GPIO.LOW)
        pwm_B.start(abs(vitesse_droite))
    elif vitesse_droite < 0:
        GPIO.output(IN3, GPIO.LOW) # anti horaire
        GPIO.output(IN4, GPIO.HIGH)
        pwm_B.start(abs(vitesse_droite))
