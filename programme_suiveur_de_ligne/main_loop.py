# Author: Giraudo Anthony, Kari Hichma, Marinho Louise, Kilian Mac Donald
# 15 mars 2018
# main_loop.py

import RPi.GPIO as GPIO
import pygame

# utiliser callback
# 5 capteurs

GPIO.setmode(GPIO.BOARD)

from classes import *

coeff = 1
gpio_capteur_centre = 11
gpio_capteur_droit = 13
gpio_capteur_gauche = 15
vitesse_de_marche = 100
inverser_sens_moteur_droit = False
inverser_sens_moteur_gauche = False
choix_1 = "droite"
choix_2 = None
gpio_pwm_roue_droite = 16
gpio_pwm_roue_gauche = 12


robot = Robot(gpio_capteur_centre, gpio_capteur_gauche, gpio_capteur_droit, vitesse_de_marche, inverser_sens_moteur_droit, inverser_sens_moteur_gauche, coeff, gpio_pwm_roue_gauche, gpio_pwm_roue_droite)

GPIO.add_event_detect(gpio_capteur_centre, GPIO.RISING, callback=lambda x: robot.actualiser_etat_capteurs(), bouncetime =20)
GPIO.add_event_detect(gpio_capteur_droit, GPIO.RISING, callback=lambda x: robot.actualiser_etat_capteurs(), bouncetime =20)
GPIO.add_event_detect(gpio_capteur_gauche, GPIO.RISING, callback=lambda x: robot.actualiser_etat_capteurs(), bouncetime =20)

while True:
    if pygame.event.type == pygame.KEYDOWN:
        if pygame.event.key == pygame.K_s:
            robot.controle_moteur(0, 0)
            GPIO.cleanup()
            break

    elif robot.capteur_gauche.est_dans_le_noir() and not robot.capteur_droit.est_dans_le_noir():
        robot.tourner_gauche()

    elif robot.capteur_droit.est_dans_le_noir() and not robot.capteur_gauche.est_dans_le_noir():
        robot.tourner_droite()

    elif robot.capteur_gauche.est_dans_le_noir() and robot.capteur_droit.est_dans_le_noir() and robot.capteur_centre.est_dans_le_noir():
        robot.gerer_intersection(choix_1, choix_2)

    elif not robot.capteur_centre.est_dans_le_noir() and not robot.capteur_droit.est_dans_le_noir() and not robot.capteur_gauche.est_dans_le_noir():
        robot.demi_tour()

    else:
        robot.tout_droit()

GPIO.cleanup()
