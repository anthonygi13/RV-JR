import time

import RPi.GPIO as GPIO
import pygame

from motor_control import *

# pourquoi ne pas avoir utilise les fonctions que vous aviez deja faite comme briques pour cette fonction ? ça rendrait le code plus compact et beacoup plus clair
# programmation haut niveau ! comprendre le code meme sans les commentaires, code auto suffisant

gauche = 0  # numero des pins a determiner et a changer !
droite = 0
centre = 0

GPIO.setmode(GPIO.BOARD)
GPIO.setup(gauche, GPIO.IN)
GPIO.setup(droite, GPIO.IN)
GPIO.setup(centre, GPIO.IN)

noir = GPIO.LOW
blanc = GPIO.HIGH

#fonction à faire:
# - tourne droite (quelle argument ?? <- pas d arguments)
# - tourne gauche
# - intersection ---------- ok <- non pas ok..., il faut pas que y ait d arguments et ça doit pas utiliser tourner droite ni tourner gauche qui servent seulement au recalibrage
# - demi tour
# - est_dans_le_noir

# Structure du programme à modifier avec les differents cas
def controle_moteur(VitesseG, VitesseD):
    pass

def est_dans_le_noir(capteur):
    return capteur == noir

def avance (VitesseG, VitesseD):
    controle_moteur(VitesseG, VitesseD)

def tourne_droite(VitesseG, VitesseD):
    controle_moteur(VitesseG, 0)

def tourne_gauche(VitesseG, VitesseD):
    controle_moteur(0, VitesseD)

def demi_tour(VitesseG, VitesseD, choix):
    if choix == 'gauche' or choix == 'centre':
        tourne_gauche(VitesseG, VitesseD)
    else :
        tourne_droite(VitesseG, VitesseD)


def actualise_capteur(num_capteur):
    return GPIO.input(num_capteur)

def intersection(VitesseG, VitesseD, choix): #le choix peut aussi être 'centre', auquel cas le robot ira en face
    if choix =='droite':
        while est_dans_le_noir(gauche)==True:
            tourne_droite(VitesseG, VitesseD)
    if choix=='centre':
        while est_dans_le_noir(gauche)==True and est_dans_le_noir(droite)==True
            avance(VitesseG, VitesseG)
    else:
        while est_dans_le_noir(droite)==True:
            tourne_gauche(VitesseG, VitesseD)





# parametrer capter blanc et capter noir
def SuivreLigne(constante, VitesseD, VitesseG, choix): #il va falloir modifier les cas non ?
    capteurG = actualise_capteur(gauche)
    capteurC = actualise_capteur(centre)
    capteurD = actualise_capteur(droite)

    while True:  # boucle infinie, on n'a pas de cas terminal pour l'instant (à voir plus tard...) STOP AVEC CLAVIER
        if pygame.event.type == pygame.KEYDOWN:
            if pygame.event.key == pygame.K_s:
                controle_moteur(0, 0)
                break

        elif not est_dans_le_noir(capteurG) and est_dans_le_noir(capteurC) and not est_dans_le_noir(capteurD):
            avance(VitesseD, VitesseG)

        elif est_dans_le_noir(capteurG) and est_dans_le_noir(capteurC) and not est_dans_le_noir(capteurD) :
            tourne_gauche(VitesseG, VitesseD)

        elif not est_dans_le_noir(capteurG) and est_dans_le_noir(capteurC) and est_dans_le_noir(capteurD):
            tourne_droite(VitesseG, VitesseD)

        elif est_dans_le_noir(capteurG) and est_dans_le_noir(capteurC) and est_dans_le_noir(capteurD) :
            intersection(VitesseD, VitesseG, choix)

        elif not est_dans_le_noir(capteurC) :
            demi_tour(VitesseG, VitesseD, choix)

        capteurG = actualise_capteur(gauche)
        capteurC = actualise_capteur(centre)
        capteurD = actualise_capteur(droite)



'''''''''''

        while capteurC == GPIO.HIGH:
            if capteurD == GPIO.HIGH and capteurG == GPIO.LOW:  # tourner à droite
                T = time.clock()
                while capteurD == GPIO.HIGH:
                    # si jamais on est a une intersection en croix, et que le robot detecte la brnche
                    # droite une fraction de seconde avant bah la il va tourner a droite...
                    t = time.clock()
                    controle_moteur(VitesseG, VitesseD - constante * (t - T))  # a voir si on continue comme ça
                    capteurD = GPIO.input(droite)

            elif capteurG == GPIO.HIGH and capteurD == GPIO.LOW:  # tourner à gauche #capteurG peut pas etre a la fois LOW et HIGH
                T = time.clock()
                while capteurG == GPIO.HIGH:
                    # si jamais on est a une intersection en croix, et que le robot detecte la brnche
                    # gauche une fraction de seconde avant bah la il va tourner a gauche...
                    t = time.clock()
                    controle_moteur(VitesseG - constante * (t - T), VitesseD)
                    capteurG = GPIO.input(gauche)

            elif capteurD == GPIO.LOW and capteurG == GPIO.LOW:  # continuer tout droit
                controle_moteur(VitesseG, VitesseD)
                capteurG = GPIO.input(gauche)
                capteurD = GPIO.input(droite)
                capteurC = GPIO.input(centre)

            else:  # intersection = traité plus bas
                break

        # tous les capteurs sont dans le noir = intersection
        # choix = choix de là où le robot tourne = 'gauche', 'droite' ou 'centre'

        if capteurD == GPIO.HIGH and capteurC == GPIO.HIGH:  # capteurG faut pas qu'il soit dans le noir ?
            est_passe_blanc = False  # variable permettant de savoir si le capteur centrale est déjà passé dans le blanc ou pas
            while not est_passe_blanc or capteurC != GPIO.HIGH:  # la boucle s'arrête lorsque le capteur revient dans le noir après être passé par le blanc
                if choix == 'gauche':
                    controle_moteur(-VitesseG, VitesseD)
                elif choix == 'droite':
                    controle_moteur(VitesseG, -VitesseD)
                else:
                    controle_moteur(VitesseG, VitesseD)
                    capteurC = GPIO.input(centre)

                if capteurC == GPIO.LOW:
                    est_passe_blanc = True

        # tous les capteurs sont dans le blanc => demi-tour
        # y a aucune condition qui dit que tout les capteurs sont dans le blanc la
        while capteurC != GPIO.HIGH:
            if choix == 'gauche' or choix == 'centre':  # a quoi sert le choix ? c pas juste un demi tour ?
                controle_moteur(-VitesseG, VitesseD)
            else:
                controle_moteur(VitesseG, -VitesseD)
                capteurC = GPIO.input(centre)
'''''''''''