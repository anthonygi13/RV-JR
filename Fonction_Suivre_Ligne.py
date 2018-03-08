import time

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
import pygame

from motor_control import *

# pourquoi ne pas avoir utilise les fonctions que vous aviez deja faite comme briques pour cette fonction ? ça rendrait le code plus compact et beacoup plus clair
# programmation haut niveau ! comprendre le code meme sans les commentaires, code auto suffisant

#DEFITION DES PARAMETRES (valeurs à rentrer ici)

gauche = 0  # numero des pins a determiner et a changer !
droite = 0
centre = 0

GPIO.setmode(GPIO.BOARD)
capteurG = GPIO.setup(gauche, GPIO.IN)
capteurD = GPIO.setup(droite, GPIO.IN)
capteurC = GPIO.setup(centre, GPIO.IN)

noir = GPIO.LOW
blanc = GPIO.HIGH

########################################################################

#FONCTIONS (hormis changements dans les fonctions, on ne devrait pas avoir à modifier quoi que ce soit ici)

# fonction à faire:
# - tourne droite (quelle argument ?? <- pas d arguments)
# - tourne gauche
# - intersection ---------- ok <- non pas ok..., il faut pas que y ait d arguments et ça doit pas utiliser tourner droite ni tourner gauche qui servent seulement au recalibrage
# - demi tour
# - est_dans_le_noir

# Structure du programme à modifier avec les differents cas

def actualise_capteurs(capteurG, capteurC, capteurD):
    capteurG = GPIO.input()  # Faudra mettre le numéro des pins des capteurs correpondant dans les parenthèses
    capteurC = GPIO.input()
    capteurD = GPIO.input()

def est_dans_le_noir(capteur):
    return capteur == noir


def avance(VitesseG, VitesseD):
    controle_moteur(VitesseG, VitesseD)


def tourne_droite(VitesseG, VitesseD):
    controle_moteur(VitesseG, 0)


def tourne_gauche(VitesseG, VitesseD):
    controle_moteur(0, VitesseD)


def demi_tour(VitesseG, VitesseD, choix):
    if choix == 'gauche' or choix == 'centre':
        tourne_gauche(VitesseG, VitesseD)
    else:
        tourne_droite(VitesseG, VitesseD)


# Pareil, faudra mettre le numéro des pins des capteurs à la place des '??', chaque pin dans chaque cas
# (par exemple) :
GPIO.add_event_detect('??', GPIO.RISING, callback=actualise_capteurs)  # pin de capteurG
GPIO.add_event_detect('??', GPIO.RISING, callback=actualise_capteurs)  # pin de capteurC
GPIO.add_event_detect('??', GPIO.RISING, callback=actualise_capteurs)  # pin de capteurD

GPIO.add_event_detect('??', GPIO.FALLING, callback=actualise_capteurs)  # pin de capteurG
GPIO.add_event_detect('??', GPIO.FALLING, callback=actualise_capteurs)  # pin de capteurC
GPIO.add_event_detect('??', GPIO.FALLING, callback=actualise_capteurs)  # pin de capteurD


def intersection(VitesseG, VitesseD, choix):  # le choix peut aussi être 'centre', auquel cas le robot ira en face
    if choix == 'droite':
        while est_dans_le_noir(gauche) == True:
            tourne_droite(VitesseG, VitesseD)
    if choix == 'centre':
        while est_dans_le_noir(gauche) == True and est_dans_le_noir(droite) == True
            avance(VitesseG, VitesseG)
    else:
        while est_dans_le_noir(droite) == True:
            tourne_gauche(VitesseG, VitesseD)


# parametrer capteur blanc et capteur noir

def SuivreLigne(constante, VitesseD, VitesseG, choix):  # il va falloir modifier les cas non ?
    global capteurG, capteurC, capteurD
    actualise_capteurs(capteurG, capteurC, capteurD)

    while True:  # boucle infinie, on n'a pas de cas terminal pour l'instant (à voir plus tard...) STOP AVEC CLAVIER
        if pygame.event.type == pygame.KEYDOWN:
            if pygame.event.key == pygame.K_s:
                controle_moteur(0, 0)
                break

        elif not est_dans_le_noir(capteurG) and est_dans_le_noir(capteurC) and not est_dans_le_noir(capteurD):
            avance(VitesseD, VitesseG)

        elif est_dans_le_noir(capteurG) and est_dans_le_noir(capteurC) and not est_dans_le_noir(capteurD):
            tourne_gauche(VitesseG, VitesseD)

        elif not est_dans_le_noir(capteurG) and est_dans_le_noir(capteurC) and est_dans_le_noir(capteurD):
            tourne_droite(VitesseG, VitesseD)

        elif est_dans_le_noir(capteurG) and est_dans_le_noir(capteurC) and est_dans_le_noir(capteurD):
            intersection(VitesseD, VitesseG, choix)

        elif not est_dans_le_noir(capteurC):
            demi_tour(VitesseG, VitesseD, choix)

        actualise_capteurs(capteurG, capteurC, capteurD)
