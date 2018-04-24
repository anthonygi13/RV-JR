# Authors: Giraudo Anthony, Kari Hichma, Marinho Louise, Kilian Mac Donald
# 15 mars 2018
# main_loop.py

import RPi.GPIO as GPIO
import pygame
from pygame.locals import *
pygame.init()
from classes import *


GPIO.setmode(GPIO.BOARD) # precise la convention de numerotation des broches a utiliser


# parametres

distance_roues = 15 # en cm
largeur_chemin = 3 # en cm
coeff = 1
gpio_capteur_centre = 11
gpio_capteur_interieur_droit = 13
gpio_capteur_interieur_gauche = 15
gpio_capteur_exterieur_droit = 18
gpio_capteur_exterieur_gauche = 35
gpio_IN1 = 32
gpio_IN2 = 36
gpio_IN3 = 40
gpio_IN4 = 37
gpio_pwm_roue_droite = 16
gpio_pwm_roue_gauche = 12
vitesse_de_marche = 50 # en pourcentage de la vitesse maximale que peuvent atteindre les roues
inverser_sens_moteur_droit = True
inverser_sens_moteur_gauche = True
choix = "tout droit"


robot = Robot(gpio_capteur_centre, gpio_capteur_interieur_gauche, gpio_capteur_interieur_droit, gpio_capteur_exterieur_gauche, gpio_capteur_exterieur_droit, vitesse_de_marche, inverser_sens_moteur_droit, inverser_sens_moteur_gauche, coeff, gpio_pwm_roue_gauche, gpio_pwm_roue_droite, largeur_chemin, distance_roues, gpio_IN1, gpio_IN2, gpio_IN3, gpio_IN4)


# actualise constamment l etat des capteurs

GPIO.add_event_detect(gpio_capteur_centre, GPIO.RISING, callback=lambda x: robot.actualiser_etat_capteurs(), bouncetime=20)
GPIO.add_event_detect(gpio_capteur_interieur_droit, GPIO.RISING, callback=lambda x: robot.actualiser_etat_capteurs(), bouncetime=20)
GPIO.add_event_detect(gpio_capteur_interieur_gauche, GPIO.RISING, callback=lambda x: robot.actualiser_etat_capteurs(), bouncetime=20)


continuer = True

while continuer: # boucle principale
    """
    for event in pygame.event.get(): # arreter le robot si la touche s est pressee
        if pygame.event.type == pygame.KEYDOWN:
            if pygame.event.key == pygame.K_s:
                robot.stop()
                continuer = False
    """
    if continuer:

        if robot.capteur_interieur_gauche.est_dans_le_noir() and not robot.capteur_interieur_droit.est_dans_le_noir():
            robot.tourner_gauche()

        elif robot.capteur_interieur_droit.est_dans_le_noir() and not robot.capteur_interieur_gauche.est_dans_le_noir():
            robot.tourner_droite()

        elif robot.capteur_interieur_gauche.est_dans_le_noir() and robot.capteur_exterieur_gauche.est_dans_le_noir() and\
                robot.capteur_interieur_droit.est_dans_le_noir() and robot.capteur_exterieur_droit.est_dans_le_noir() and robot.capteur_centre.est_dans_le_noir():
            robot.stop()
            continuer = False

        elif robot.capteur_interieur_gauche.est_dans_le_noir() and robot.capteur_interieur_droit.est_dans_le_noir() and robot.capteur_centre.est_dans_le_noir():
            robot.gerer_intersection(choix)

        elif not robot.capteur_centre.est_dans_le_noir() and not robot.capteur_interieur_droit.est_dans_le_noir() and not robot.capteur_interieur_gauche.est_dans_le_noir():
            continuer = robot.demi_tour()

        else:
            robot.tout_droit()

GPIO.cleanup() # reinitialise l etat des broches
pygame.quit()

