# Authors: Giraudo Anthony, Kari Hichma, Marinho Louise, Kilian Mac Donald
# 15 mars 2018
# classes.py

import RPi.GPIO as GPIO
import pygame
from pygame.locals import *
pygame.init()

class Capteur: # classe permettant de gerer l etat des capteurs

    def __init__(self, gpio):
        """
        :param gpio: numero de la broche recevant du signal du capteur
        """

        self.gpio = gpio
        GPIO.setup(gpio, GPIO.IN)
        self.etat = GPIO.input(gpio)

    def actualiser_etat(self): # actualise l etat du capteur

        self.etat = GPIO.input(self.gpio)

    def est_dans_le_noir(self):
        """
        :return: True si le capteur detecte du noir et Flase sinon
        """

        return not self.etat == GPIO.LOW

class Robot: # classe permettant de controler le robot

    def __init__(self, gpio_capteur_centre, gpio_capteur_interieur_gauche, gpio_capteur_interieur_droit, gpio_capteur_exterieur_gauche, gpio_capteur_exterieur_droit, vitesse_de_marche, inverser_sens_moteur_gauche, inverser_sens_moteur_droit, coeff, gpio_pwm_roue_gauche, gpio_pwm_roue_droite, largeur_chemin, distance_roues, gpio_IN1, gpio_IN2, gpio_IN3, gpio_IN4):
        """
        :param gpio_capteur_centre: numero de la broche recevant du signal du capteur central
        :param gpio_capteur_interieur_gauche: numero de la broche recevant du signal du capteur interieur gauche
        :param gpio_capteur_interieur_droit: numero de la broche recevant du signal du capteur interieur droit
        :param gpio_capteur_exterieur_gauche: numero de la broche recevant du signal du capteur exterieur gauche
        :param gpio_capteur_exterieur_droit: numero de la broche recevant du signal du capteur exterieur droit
        :param vitesse_de_marche: vitesse du robot lorsqu il va tout droit, en pourcentage de la vitesse maximale que peuvent atteindre les roues
        :param inverser_sens_moteur_gauche: booleen indiquant si le sens de rotation du moteur gauche doit etre inverse
        :param inverser_sens_moteur_droit: booleen indiquant si le sens de rotation du moteur droit doit etre inverse
        :param coeff: coefficient multiplicatif utilise pour les methodes gerer_intersection, tourner_droite et tourner_gauche
        :param gpio_pwm_roue_gauche: numero de la broche reliee a l entree ENA du double pont en H et qui permet le controle du moteur gauche
        :param gpio_pwm_roue_droite: numero de la broche reliee a l entree ENB du double pont en H et qui permet le controle du moteur droit
        :param largeur_chemin: largeur du chemin suivi en cm
        :param distance_roues: distances entre les deux roues en cm
        :param gpio_IN1: numero de la broche reliee a l entree IN1 du double pont en H (liee au controle du moteur gauche)
        :param gpio_IN2: numero de la broche reliee a l entree IN2 du double pont en H (liee au controle du moteur gauche)
        :param gpio_IN3: numero de la broche reliee a l entree IN3 du double pont en H (liee au controle du moteur droit)
        :param gpio_IN4: numero de la broche reliee a l entree IN4 du double pont en H (liee au controle du moteur droit)
        """

        self.capteur_centre = Capteur(gpio_capteur_centre)
        self.capteur_interieur_droit = Capteur(gpio_capteur_interieur_droit)
        self.capteur_interieur_gauche = Capteur(gpio_capteur_interieur_gauche)
        self.capteur_exterieur_droit = Capteur(gpio_capteur_exterieur_droit)
        self.capteur_exterieur_gauche = Capteur(gpio_capteur_exterieur_gauche)
        self.vitesse = vitesse_de_marche
        self.vitesse_droite = vitesse_de_marche
        self.vitesse_gauche = vitesse_de_marche
        self.inverser_sens_moteur_droit = inverser_sens_moteur_droit
        self.inverser_sens_moteur_gauche = inverser_sens_moteur_gauche
        self.coeff = coeff
        self.gpio_pwm_roue_gauche = gpio_pwm_roue_gauche
        self.gpio_pwm_roue_droite = gpio_pwm_roue_droite
        GPIO.setup(gpio_pwm_roue_droite, GPIO.OUT, initial=GPIO.LOW) # initialisation
        GPIO.setup(gpio_pwm_roue_gauche, GPIO.OUT, initial=GPIO.LOW) # initialisation
        self.pwm_roue_droite = GPIO.PWM(gpio_pwm_roue_droite, 8) # initialisation
        self.pwm_roue_gauche = GPIO.PWM(gpio_pwm_roue_gauche, 8) # initialisation
        self.pwm_roue_droite.start(0) # initialisation
        self.pwm_roue_gauche.start(0) # initialisation
        self.largeur_chemin = largeur_chemin
        self.distance_roues = distance_roues
        self.gpio_IN1 = gpio_IN1
        self.gpio_IN2 = gpio_IN2
        self.gpio_IN3 = gpio_IN3
        self.gpio_IN4 = gpio_IN4
        GPIO.setup(gpio_IN1, GPIO.OUT, initial=GPIO.LOW) # initialisation
        GPIO.setup(gpio_IN2, GPIO.OUT, initial=GPIO.LOW) # initialisation
        GPIO.setup(gpio_IN3, GPIO.OUT, initial=GPIO.LOW) # initialisation
        GPIO.setup(gpio_IN4, GPIO.OUT, initial=GPIO.LOW) # initialisation

    def controle_moteur(self, vitesse_gauche, vitesse_droite): # controle les vitesses des roues
        """
        :param vitesse_gauche: en pourcentage (de -100 a 100). Une vitesse negative correspond à une rotation vers l arriere
        :param vitesse_droite: en pourcentage (de -100 a 100). Une vitesse negative correspond à une rotation vers l arriere
        """

        if self.inverser_sens_moteur_gauche:
            vitesse_gauche = -vitesse_gauche
        if self.inverser_sens_moteur_droit:
            vitesse_droite = -vitesse_droite

        self.vitesse_droite = vitesse_droite
        self.vitesse_gauche = vitesse_gauche

        if vitesse_gauche > 0:
            GPIO.output(self.gpio_IN1, GPIO.HIGH)  # rotation sens horaire
            GPIO.output(self.gpio_IN2, GPIO.LOW)
            self.pwm_roue_gauche.ChangeDutyCycle(abs(vitesse_gauche))
        elif vitesse_gauche < 0:
            GPIO.output(self.gpio_IN1, GPIO.LOW)  # anti horaire
            GPIO.output(self.gpio_IN2, GPIO.HIGH)
            self.pwm_roue_gauche.ChangeDutyCycle(abs(vitesse_gauche))

        if vitesse_droite > 0:
            GPIO.output(self.gpio_IN3, GPIO.HIGH)  # rotation sens horaire
            GPIO.output(self.gpio_IN4, GPIO.LOW)
            self.pwm_roue_droite.ChangeDutyCycle(abs(vitesse_droite))
        elif vitesse_droite < 0:
            GPIO.output(self.gpio_IN3, GPIO.LOW)  # anti horaire
            GPIO.output(self.gpio_IN4, GPIO.HIGH)
            self.pwm_roue_droite.ChangeDutyCycle(abs(vitesse_droite))

    def tourner_gauche(self): # change les vitesses des roues pour rectifier la trajectoire du robot vers la gauche

        K = 2 * self.largeur_chemin
        self.controle_moteur(self.vitesse * self.coeff * (2 * K - self.distance_roues) / (2 * K + self.distance_roues),
                             self.vitesse * self.coeff)

    def tourner_droite(self): # change les vitesses des roues pour rectifier la trajectoire du robot vers la droite

        K = 2 * self.largeur_chemin
        self.controle_moteur(self.vitesse * self.coeff,
                             self.vitesse * self.coeff * (2 * K - self.distance_roues) / (2 * K + self.distance_roues))

    def demi_tour(self): # fait faire un demi tour au robot tant que le capteur central ne detecte pas de noir
        """
        :return: True si la touche d arret n a pas ete pressee, False sinon
        """

        stop = False
        self.controle_moteur(self.vitesse * self.coeff, -self.vitesse * self.coeff)
        while not self.capteur_centre.est_dans_le_noir():
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:  # stopper le robot en cas d appui sur la touche s
                        stop = True
            if stop:
                self.stop()
                return False
        return True

    def gerer_intersection(self, choix): # change les vitesses des roues pour que le robot aille dans la direction voulue a une intersection
        """
        :param choix: chaine de caracteres correspondant au choix de la direction a prendre a l intersection,
         "droite", "gauche" ou "tout droit"
        """

        if not choix in ["droite", "gauche", "tout droit"]:
            raise ValueError("Le choix n est pas valide")

        K = 102 / 109 * self.largeur_chemin

        if choix == "droite":
            self.controle_moteur(self.vitesse * self.coeff,
                                 self.vitesse * self.coeff * (2 * K - self.distance_roues) / (2 * K + self.distance_roues))

        elif choix == "gauche":
            self.controle_moteur(self.vitesse * self.coeff * (2 * K - self.distance_roues) / (2 * K + self.distance_roues),
                                 self.vitesse * self.coeff)

        elif choix == "tout droit":
            self.controle_moteur(self.vitesse, self.vitesse)

    def tout_droit(self): # change les vitesses des roues pour que le robot aille tout droit a la vitesse self.vitesse

        self.controle_moteur(self.vitesse, self.vitesse)

    def stop(self): # stoppe le mouvement du robot

        self.controle_moteur(0, 0)

    def actualiser_etat_capteurs(self): # actualise l etat des capteurs

        self.capteur_centre.actualiser_etat()
        self.capteur_interieur_gauche.actualiser_etat()
        self.capteur_interieur_droit.actualiser_etat()
        self.capteur_exterieur_gauche.actualiser_etat()
        self.capteur_exterieur_droit.actualiser_etat()

