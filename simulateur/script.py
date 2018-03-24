# Author: Giraudo Anthony, Kari Hichma, Mac Donald Kilian, Marhino Louise
# 19 février 2018
# script.py

import pygame
from pygame.locals import *
pygame.init()
import time

from fonctions import *
from classes import *

terrain = Terrain("blanc.jpg")

#terrain.ajouter_ellipse(800, 300, 50, 900, 500)

terrain.ajouter_rectangle((1600, 50), 0, 500)
terrain.ajouter_rectangle((50, 1000), 900, 0)

#terrain.ajouter_rectangle((1000, 50), 0, 500)
#terrain.ajouter_rectangle((50, 1000), 1000, 0)

robot = Robot("champi.png", "r2d2.jpg", (75, 75), (49, 49), 200, 55, 50, 75, pixel(0.2), 100)

#ne pas effacer, cette configuration marche parfaitement meme si elle a ete trouvee au hasard, r doit pas etre 0 sinon c moche, mais peut etre petit et tout marche (la r = largeur route et c bon)
# aussi, d doit etre tres proche de largeur_route, ca pose pas de soucis et ca evite les deviation trop grande difficile a gerer quand on reflechit a l algo (ici d = 110 pourcents de largeur_route)
# z = 3/2 * largeur de la route m a l air pas mal
# l = 4 fois largeur_route
#gere pas les virages a angle droit

robot.placer(0, 500)
robot.rotation(3 * 90)

robot.roue_gauche.image.set_colorkey((0,0,0))
robot.roue_droite.image.set_colorkey((0,0,0))
robot.capteur_droit.image.set_colorkey((255, 255, 255))
robot.capteur_gauche.image.set_colorkey((255, 255, 255))
robot.capteur_centre.image.set_colorkey((255, 255, 255))

v = pixel(0.2)
choix = "droite"
choix2 = "droite"

continuer = True
while continuer == True:

    t_i = time.clock()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False

    terrain.afficher()
    robot.afficher()
    pygame.display.flip()

    if event.type == KEYDOWN:
        if event.key == K_s:
            robot.vitesse_gauche = 0
            robot.vitesse_droite = 0
            #print(terrain.signal(robot.capteur_centre))
        if event.key == K_m:
            robot.rotation(10)

    elif terrain.signal(robot.capteur_droit) and not terrain.signal(robot.capteur_gauche):
        robot.vitesse_gauche = v * 100
        robot.vitesse_droite = 0

    elif terrain.signal(robot.capteur_gauche) and not terrain.signal(robot.capteur_droit):
        robot.vitesse_droite = v * 100
        robot.vitesse_gauche = 0

    elif terrain.signal(robot.capteur_gauche) and terrain.signal(robot.capteur_droit) and terrain.signal(robot.capteur_centre):
        if choix == "droite":
            robot.vitesse_gauche = v * 100
            robot.vitesse_droite = - (robot.vitesse_gauche * (robot.l - robot.d)) / (2 * robot.l)
        elif choix == "gauche":
            robot.vitesse_droite = v * 100
            robot.vitesse_gauche = - (robot.vitesse_droite * (robot.l - robot.d)) / (2 * robot.l)
        elif choix == "tout droit":
            robot.vitesse_droite = v
            robot.vitesse_gauche = v


    elif not terrain.signal(robot.capteur_centre):
        while not terrain.signal(robot.capteur_centre):
            t_i = time.clock()
            terrain.afficher()
            robot.afficher()
            pygame.display.flip()
            if choix == "tout droit":
                if choix2 == "droite":
                    robot.vitesse_gauche = v * 100
                    robot.vitesse_droite = - (robot.vitesse_gauche * (robot.l - robot.d)) / (2 * robot.l)
                elif choix2 == "gauche":
                    robot.vitesse_droite = v * 100
                    robot.vitesse_gauche = - (robot.vitesse_droite * (robot.l - robot.d)) / (2 * robot.l)
            else:
                robot.vitesse_droite = - v *100
                robot.vitesse_gauche = v * 100
            robot.mouvement(time.clock() - t_i)

    else:
        robot.vitesse_gauche = v
        robot.vitesse_droite = v

    print(robot.vitesse_gauche)

    robot.mouvement(time.clock() - t_i)


pygame.quit()