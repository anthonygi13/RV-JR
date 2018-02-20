import time

import RPi.GPIO as GPIO

def controle_moteur (VitesseG, VitesseD):
    pass
gauche = 1 #numéro des pins à vérifier
droite = 2
centre = 3

GPIO.setmode(GPIO.BOARD)
GPIO.setup(gauche,GPIO.IN)
GPIO.setup(droite, GPIO.IN)
GPIO.setup(centre, GPIO.IN)

def SuivreLigne (capteurG, capteurC, capteurD, constante, VitesseD, VitesseG, choix):
    while True: #boucle infinie, on n'a pas de cas terminal pour l'instant (à voir plus tard...)
        while capteurC == GPIO.HIGH:
            if capteurD == GPIO.HIGH and capteurG == GPIO.LOW: #tourner à droite
                T = time.clock()
                while capteurD == 1:
                    t = time.clock()
                    controle_moteur(VitesseG, VitesseD - constante * (t - T))
                    capteurD = input(capteurD)

            elif capteurG == 1 and capteurG == 0: #tourner à gauche
                T = time.clock()
                while capteurG == 1:
                    t = time.clock()
                    controle_moteur(VitesseG - constante * (t - T), VitesseD)
                    capteurG = input(capteurG)

            elif capteurD == 0 and capteurG == 0: #continuer tout droit
                controle_moteur(VitesseG, VitesseD)
                capteurG = input(capteurG)
                capteurD = input(capteurD)

            else:
                break

        # tous les capteurs sont dans le noir = intersection
        #choix = choix de là où le capteur tourne = 'gauche', 'droite' ou 'centre'
        if capteurD == 1 and capteurC == 1 :
            est_passe_blanc = False #variable permettant de savoir si le capteur centrale est déjà passé dans le blanc ou pas
            while not est_passe_blanc or capteurC != 1: #la boucle s'arrête lorsque le capteur revient dans le noir après être passé par le blanc
                if choix == 'gauche':
                    controle_moteur(-VitesseG, VitesseD)
                elif choix == 'droite':
                    controle_moteur(VitesseG, -VitesseD)
                else:
                    controle_moteur(VitesseG, VitesseD)
                    capteurC == input(capteurC)

                if capteurC == 0:
                    est_passe_blanc = True


        #tous les capteurs sont dans le blanc = demi-tour
        while capteurC != 1:
            if choix == 'gauche' or choix == 'centre':
                controle_moteur(-VitesseG, VitesseD)
            else:
                controle_moteur(VitesseG, -VitesseD)
                capteurC = input(capteurC)
































