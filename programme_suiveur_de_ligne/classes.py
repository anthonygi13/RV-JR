# Author: Giraudo Anthony, Kari Hichma, Marinho Louise, kilian Mac Donald
# 15 mars 2018
# classes.py

import RPi.GPIO as GPIO

class Capteur:
    def __init__(self, gpio):
        self.gpio = gpio
        GPIO.setup(gpio, GPIO.IN)
        self.etat = GPIO.input(gpio)

    def actualiser_etat(self):
        self.etat = GPIO.input(self.gpio)

    def est_dans_le_noir(self):
        return not self.etat == GPIO.LOW

class Robot:

    def __init__(self, gpio_capteur_centre, gpio_capteur_interieur_gauche, gpio_capteur_interieur_droit, gpio_capteur_exterieur_gauche, gpio_capteur_exterieur_droit, vitesse_de_marche, inverser_sens_moteur_gauche, inverser_sens_moteur_droit, coeff, gpio_pwm_roue_gauche, gpio_pwm_roue_droite, largeur_chemin, distance_roues, gpio_IN1, gpio_IN2, gpio_IN3, gpio_IN4):
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
        GPIO.setup(gpio_pwm_roue_droite, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(gpio_pwm_roue_gauche, GPIO.OUT, initial=GPIO.LOW)
        self.pwm_roue_droite = GPIO.PWM(gpio_pwm_roue_droite, 8)
        self.pwm_roue_gauche = GPIO.PWM(gpio_pwm_roue_gauche, 8)
        self.pwm_roue_droite.start(0)
        self.pwm_roue_gauche.start(0)
        self.largeur_chemin = largeur_chemin
        self.distance_roues = distance_roues
        self.gpio_IN1 = gpio_IN1
        self.gpio_IN2 = gpio_IN2
        self.gpio_IN3 = gpio_IN3
        self.gpio_IN4 = gpio_IN4


    def controle_moteur(self, vitesse_gauche, vitesse_droite):
        """
        :param vitesse_gauche: en pourcentage (de -100 a 100)
        :param vitesse_droite: en pourcentage (de -100 a 100)
        :return: None, controle la vitesse des roues. Une vitesse negative correspond à une rotation vers l'arriere
        """

        if self.inverser_sens_moteur_gauche:
            vitesse_gauche = -vitesse_gauche
        if self.inverser_sens_moteur_droit:
            vitesse_droite = -vitesse_droite

        self.vitesse_droite = vitesse_droite
        self.vitesse_gauche = vitesse_gauche

        IN1 = self.gpio_IN1
        IN2 = self.gpio_IN2
        IN3 = self.gpio_IN3
        IN4 = self.gpio_IN4

        GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(IN2, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(IN3, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(IN4, GPIO.OUT, initial=GPIO.LOW)

        if vitesse_gauche > 0:
            GPIO.output(IN1, GPIO.HIGH)  # rotation sens horaire
            GPIO.output(IN2, GPIO.LOW)
            self.pwm_roue_gauche.ChangeDutyCycle(abs(vitesse_gauche))
        elif vitesse_gauche < 0:
            GPIO.output(IN1, GPIO.LOW)  # anti horaire
            GPIO.output(IN2, GPIO.HIGH)
            self.pwm_roue_gauche.ChangeDutyCycle(abs(vitesse_gauche))

        if vitesse_droite > 0:
            GPIO.output(IN3, GPIO.HIGH)  # rotation sens horaire
            GPIO.output(IN4, GPIO.LOW)
            self.pwm_roue_droite.ChangeDutyCycle(abs(vitesse_droite))
        elif vitesse_droite < 0:
            GPIO.output(IN3, GPIO.LOW)  # anti horaire
            GPIO.output(IN4, GPIO.HIGH)
            self.pwm_roue_droite.ChangeDutyCycle(abs(vitesse_droite))

    def tourner_gauche(self):
        self.controle_moteur(0, self.vitesse * self.coeff)

    def tourner_droite(self):
        self.controle_moteur(self.vitesse * self.coeff, 0)

    def demi_tour(self):
        self.controle_moteur(self.vitesse * self.coeff, -self.vitesse * self.coeff)
        while not self.capteur_centre.est_dans_le_noir():
            pass

    def gerer_intersection(self, choix):
        if choix == "droite":
            #self.controle_moteur(self.vitesse * self.coeff, -(self.vitesse * self.coeff * 0.3625)) #(l-d)/2l = 0.3625
            self.controle_moteur(self.vitesse * self.coeff, self.vitesse * self.coeff * (2 * 4.275 * self.largeur_chemin - self.distance_roues) / (2 * 4.275 * self.largeur_chemin + self.distance_roues))
        elif choix == "gauche":
            self.controle_moteur(-(self.vitesse * self.coeff * 0.3625), self.vitesse * self.coeff)
        elif choix == "tout droit":
            self.controle_moteur(self.vitesse, self.vitesse)

    def tout_droit(self):
        self.controle_moteur(self.vitesse, self.vitesse)

    def stop(self):
        self.controle_moteur(0, 0)

    def actualiser_etat_capteurs(self):
        self.capteur_centre.actualiser_etat()
        self.capteur_interieur_gauche.actualiser_etat()
        self.capteur_interieur_droit.actualiser_etat()
        self.capteur_exterieur_gauche.actualiser_etat()
        self.capteur_exterieur_droit.actualiser_etat()