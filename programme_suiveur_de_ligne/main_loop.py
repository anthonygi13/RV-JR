# Author: Giraudo Anthony, Kari Hichma, Marinho Louise, Kilian Mac Donald
# 15 mars 2018
# main_loop.py

import RPi.GPIO as GPIO
import pygame
from classes import *

GPIO.setmode(GPIO.BOARD) # precise la numerotation des pins a utiliser


# parametres

distance_roues = 15 # en cm
largeur_chemin = 3 # en cm
coeff = 1
gpio_capteur_centre = 11
gpio_capteur_interieur_droit = 13
gpio_capteur_interieur_gauche = 15
gpio_capteur_exterieur_droit = 0 # a determiner
gpio_capteur_exterieur_gauche = 0 # a determiner
vitesse_de_marche = 100
inverser_sens_moteur_droit = False
inverser_sens_moteur_gauche = False
gpio_pwm_roue_droite = 16
gpio_pwm_roue_gauche = 12
choix = "droite"


robot = Robot(gpio_capteur_centre, gpio_capteur_interieur_gauche, gpio_capteur_interieur_droit, gpio_capteur_exterieur_gauche, gpio_capteur_exterieur_droit, vitesse_de_marche, inverser_sens_moteur_droit, inverser_sens_moteur_gauche, coeff, gpio_pwm_roue_gauche, gpio_pwm_roue_droite, largeur_chemin, distance_roues)

GPIO.add_event_detect(gpio_capteur_centre, GPIO.RISING, callback=lambda x: robot.actualiser_etat_capteurs(), bouncetime=20)
GPIO.add_event_detect(gpio_capteur_interieur_droit, GPIO.RISING, callback=lambda x: robot.actualiser_etat_capteurs(), bouncetime=20)
GPIO.add_event_detect(gpio_capteur_interieur_gauche, GPIO.RISING, callback=lambda x: robot.actualiser_etat_capteurs(), bouncetime=20)

while True:
    if pygame.event.type == pygame.KEYDOWN:
        if pygame.event.key == pygame.K_s:
            robot.stop()
            break

    elif robot.capteur_gauche.est_dans_le_noir() and not robot.capteur_droit.est_dans_le_noir():
        robot.tourner_gauche()

    elif robot.capteur_droit.est_dans_le_noir() and not robot.capteur_gauche.est_dans_le_noir():
        robot.tourner_droite()

    elif robot.capteur_interieur_gauche.est_dans_le_noir() and robot.capteur_exterieur_gauche.est_dans_le_noir() and\
            robot.capteur_interieur_droit.est_dans_le_noir() and robot.capteur_exterieur_droit.est_dans_le_noir() and robot.capteur_centre.est_dans_le_noir():
        robot.stop()
        break

    elif robot.capteur_gauche.est_dans_le_noir() and robot.capteur_droit.est_dans_le_noir() and robot.capteur_centre.est_dans_le_noir():
        robot.gerer_intersection(choix)

    elif not robot.capteur_centre.est_dans_le_noir() and not robot.capteur_droit.est_dans_le_noir() and not robot.capteur_gauche.est_dans_le_noir():
        robot.demi_tour()

    else:
        robot.tout_droit()

GPIO.cleanup()
