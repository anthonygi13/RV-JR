import time

import RPi.GPIO as GPIO

def controle_moteur (VitesseG, VitesseD):
    pass
gauche = 1 #numéro des pins à établir parce que on sait que ça sera pas ça
droite = 2
centre = 3

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
                    t = time.clock()
                    controle_moteur(VitesseG, VitesseD - constante * (t - T))
                    capteurD = GPIO.input(droite)

            elif capteurG == GPIO.HIGH and capteurG == GPIO.LOW: #tourner à gauche
                T = time.clock()
                while capteurG == GPIO.HIGH:
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
        if capteurD == GPIO.HIGH and capteurC == GPIO.HIGH :
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
        while capteurC != GPIO.HIGH:
            if choix == 'gauche' or choix == 'centre':
                controle_moteur(-VitesseG, VitesseD)
            else:
                controle_moteur(VitesseG, -VitesseD)
                capteurC = GPIO.input(centre)
































