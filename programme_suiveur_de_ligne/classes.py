# Author: Giraudo Anthony                     
# 15 mars 2018
# classes.py

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)


class Capteur:
    def __init__(self, gpio):
        self.gpio = gpio
        GPIO.setup(gpio, GPIO.IN)

    def actualise(self):
        self.etat = GPIO.input(self.gpio)

    def est_dans_le_noir(self):
        return self.etat == GPIO.LOW

class Robot:
    #(l-d)/2l eventuellement rajouter en parametre

    def __init__(self, gpio_capteur_centre, gpio_capteur_gauche, gpio_capteur_droit, vitesse_de_marche, inverser_sens_moteur_gauche, inverser_sens_moteur_droit, coeff):
        self.capteur_centre = Capteur(gpio_capteur_centre)
        self.capteur_droit = Capteur(gpio_capteur_droit)
        self.capteur_gauche = Capteur(gpio_capteur_gauche)
        self.vitesse = vitesse_de_marche
        self.vitesse_droite = vitesse_de_marche
        self.vitesse_gauche = vitesse_de_marche
        self.inverser_sens_moteur_droit = inverser_sens_moteur_droit
        self.inverser_sens_moteur_gauche = inverser_sens_moteur_gauche
        self.coeff = coeff

    def controle_moteur(self, vitesse_gauche, vitesse_droite):
        """
        :param v_g: en pourcentage (de -100 a 100)
        :param v_d: en pourcentage (de -100 a 100)
        :return:
        A gauche
        B droite
        "-" correspond au sens "arriere"
        """
        if self.inverser_sens_moteur_gauche:
            vitesse_gauche = -vitesse_gauche
        if self.inverser_sens_moteur_droit:
            vitesse_droite = -vitesse_droite

        self.vitesse_droite = vitesse_droite
        self.vitesse_gauche = vitesse_gauche

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

        pwm_A = GPIO.PWM(ENA, 8)  # frequence a determiner
        pwm_B = GPIO.PWM(ENB, 8)

        if vitesse_gauche > 0:
            GPIO.output(IN1, GPIO.HIGH)  # rotation sens horaire
            GPIO.output(IN2, GPIO.LOW)
            pwm_A.start(abs(vitesse_gauche))
        elif vitesse_gauche < 0:
            GPIO.output(IN1, GPIO.LOW)  # anti horaire
            GPIO.output(IN2, GPIO.HIGH)
            pwm_A.start(abs(vitesse_gauche))

        if vitesse_droite > 0:
            GPIO.output(IN3, GPIO.HIGH)  # rotation sens horaire
            GPIO.output(IN4, GPIO.LOW)
            pwm_B.start(abs(vitesse_droite))
        elif vitesse_droite < 0:
            GPIO.output(IN3, GPIO.LOW)  # anti horaire
            GPIO.output(IN4, GPIO.HIGH)
            pwm_B.start(abs(vitesse_droite))

    def tourner_gauche(self):
        self.controle_moteur(0, self.vitesse * self.coeff)

    def tourner_droite(self):
        self.controle_moteur(self.vitesse * self.coeff, 0)

    def demi_tour(self):
        self.controle_moteur(self.vitesse * self.coeff, -self.vitesse * self.coeff)
        while not self.capteur_centre.est_dans_le_noir():
            pass

    def gerer_intersection(self, choix_1, choix_2=None):
        if choix_1 == "droite":
            self.controle_moteur(self.vitesse * self.coeff, -(self.vitesse * self.coeff * 0.3625)) #(l-d)/2l = 0.3625
        elif choix_1 == "gauche":
            self.controle_moteur(-(self.vitesse * self.coeff * 0.3625), self.vitesse * self.coeff)
        elif choix_1 == "tout droit":
            assert choix_2 is not None
            self.controle_moteur(self.vitesse, self.vitesse)
            while self.capteur_centre.est_dans_le_noir() and self.capteur_droit.est_dans_le_noir() and self.capteur_gauche.est_dans_le_noir():
                pass
            if not self.capteur_centre.est_dans_le_noir():
                if choix_2 == "droite":
                    self.controle_moteur(self.vitesse * self.coeff, -(self.vitesse * self.coeff * 0.3625))
                elif choix_2 == "gauche":
                    self.controle_moteur(-(self.vitesse * self.coeff * 0.3625), self.vitesse * self.coeff)
                while not self.capteur_centre.est_dans_le_noir():
                    pass

    def tout_droit(self):
        self.controle_moteur(self.vitesse, self.vitesse)


def actalise_capteurs():
    capteurAG.actualise()
    capteurG.actualise()
    capteurC.actualise()
    capteurD.actualise()
    capteurAD.actualise()

arriere_gauche = 0 # numero des pins a determiner et a changer !
gauche = 0
centre = 0
droite = 0
arriere_droite = 0

capteurAG = Capteur(arriere_gauche)
capteurG = Capteur(gauche)
capteurC = Capteur(centre)
capteurD = Capteur(droite)
capteurAD = Capteur(arriere_droite)

GPIO.add_event_detect('??', GPIO.RISING, callback=actalise_capteurs(), bouncetime =20)
GPIO.add_event_detect('??', GPIO.RISING, callback=actalise_capteurs(), bouncetime =20)
GPIO.add_event_detect('??', GPIO.RISING, callback=actalise_capteurs(), bouncetime =20)
GPIO.add_event_detect('??', GPIO.RISING, callback=actalise_capteurs(), bouncetime =20)
GPIO.add_event_detect('??', GPIO.RISING, callback=actalise_capteurs(), bouncetime =20)