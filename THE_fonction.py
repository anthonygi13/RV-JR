import time

import RPi.GPIO as GPIO

from motor_control import *

#pourquoi ne pas avoir utilise les fonctions que vous aviez deja faite comme briques pour cette fonction ? ça rendrait le code plus compact et beacoup plus clair

gauche = 0 #numero des pins a determiner et a changer !
droite = 0
centre = 0

GPIO.setmode(GPIO.BOARD)
GPIO.setup(gauche,GPIO.IN)
GPIO.setup(droite, GPIO.IN)
GPIO.setup(centre, GPIO.IN)


def SuivreLigne (constante, VitesseD, VitesseG, choix):
    capteurG = GPIO.input(gauche)
    capteurD = GPIO.input(droite)
    capteurC = GPIO.input(centre)
    while True: #boucle infinie, on n'a pas de cas terminal pour l'instant (à voir plus tard...)
        while capteurC == GPIO.HIGH:
            if capteurD == GPIO.HIGH and capteurG == GPIO.LOW: #tourner à droite
                T = time.clock()
                while capteurD == GPIO.HIGH:
		#si jamais on est a une intersection en croix, et que le robot detecte la brnche
		#droite une fraction de seconde avant bah la il va tourner a droite...
                    t = time.clock()
                    controle_moteur(VitesseG, VitesseD - constante * (t - T)) # a voir si on continue comme ça
                    capteurD = GPIO.input(droite)

            elif capteurG == GPIO.HIGH and capteurG == GPIO.LOW: #tourner à gauche #capteurG peut pas etre a la fois LOW et HIGH
                T = time.clock()
                while capteurG == GPIO.HIGH:
		    #si jamais on est a une intersection en croix, et que le robot detecte la brnche              
		    #gauche une fraction de seconde avant bah la il va tourner a gauche...
                    t = time.clock()
                    controle_moteur(VitesseG - constante * (t - T), VitesseD)
                    capteurG = GPIO.input(gauche)

            elif capteurD == GPIO.LOW and capteurG == GPIO.LOW: #continuer tout droit
                controle_moteur(VitesseG, VitesseD)
                capteurG = GPIO.input(gauche)
                capteurD = GPIO.input(droite)
                capteurC = GPIO.input(centre)

            else: #intersection = traité plus bas
                break

        # tous les capteurs sont dans le noir = intersection
        #choix = choix de là où le robot tourne = 'gauche', 'droite' ou 'centre'
        if capteurD == GPIO.HIGH and capteurC == GPIO.HIGH : #capteurG faut pas qu'il soit dans le noir ?
            est_passe_blanc = False #variable permettant de savoir si le capteur centrale est déjà passé dans le blanc ou pas
            while not est_passe_blanc or capteurC != GPIO.HIGH: #la boucle s'arrête lorsque le capteur revient dans le noir après être passé par le blanc
                if choix == 'gauche':
                    controle_moteur(-VitesseG, VitesseD)
                elif choix == 'droite':
                    controle_moteur(VitesseG, -VitesseD)
                else:
                    controle_moteur(VitesseG, VitesseD)
                    capteurC = GPIO.input(centre)

                if capteurC == GPIO.LOW:
                    est_passe_blanc = True


        #tous les capteurs sont dans le blanc => demi-tour
	#y a aucune condition qui dit que tout les capteurs sont dans le blanc la
        while capteurC != GPIO.HIGH:
            if choix == 'gauche' or choix == 'centre': #a quoi sert le choix ? c pas juste un demi tour ?
                controle_moteur(-VitesseG, VitesseD)
            else:
                controle_moteur(VitesseG, -VitesseD)
                capteurC = GPIO.input(centre)
































