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

#terrain.ajouter_rectangle((1600, 50), 0, 500)
#terrain.ajouter_rectangle((50, 1000), 900, 0)

terrain.ajouter_rectangle((1000, 50), 0, 500)
#terrain.ajouter_rectangle((50, 1000), 1000, 0)

robot = Robot("champi.png", "r2d2.jpg", (75, 75), (49, 49), 200, 55, 50, 75)

#ne pas effacer, cette configuration marche parfaitement meme si elle a ete trouvee au hasard, r doit pas etre 0 sinon c moche, mais peut etre petit et tout marche (la r = largeur route et c bon)
# aussi, d doit etre tres proche de largeur_route, ca pose pas de soucis et ca evite les deviation trop grande difficile a gerer quand on reflechit a l algo (ici d = 110 pourcents de largeur_route)
# z = 3/2 * largeur de la route m a l air pas mal
# l = 4 fois largeur_route
#gere pas les virages a angle droit

robot.placer(0, 500)
robot.rotation(3 * 90)

robot.roue_g.image.set_colorkey((0,0,0))
robot.roue_d.image.set_colorkey((0,0,0))
robot.capteur_d.image.set_colorkey((255, 255, 255))
robot.capteur_g.image.set_colorkey((255, 255, 255))
robot.capteur_c.image.set_colorkey((255, 255, 255))

v = pixel(0.05)
choix = "gauche"
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
            robot.vg = 0
            robot.vd = 0
            #print(terrain.signal(robot.capteur_c))
        if event.key == K_m:
            robot.rotation(10)

    elif terrain.signal(robot.capteur_d) and not terrain.signal(robot.capteur_g):
        print("droite")
        robot.vg = v * 100
        robot.vd = 0

    elif terrain.signal(robot.capteur_g) and not terrain.signal(robot.capteur_d):
        print("gauche")
        robot.vd = v * 100
        robot.vg = 0

    elif terrain.signal(robot.capteur_g) and terrain.signal(robot.capteur_d) and terrain.signal(robot.capteur_c):
        print("intersection")
        if choix == "droite":
            robot.vg = v * 100
            robot.vd = - (robot.vg * (robot.l - robot.d)) / (2 * robot.l)
        elif choix == "gauche":
            robot.vd = v * 100
            robot.vg = - (robot.vd * (robot.l - robot.d)) / (2 * robot.l)
        elif choix == "tout droit":
            robot.vd = v
            robot.vg = v

    elif not terrain.signal(robot.capteur_c):
        print("debut")
        while not terrain.signal(robot.capteur_c):
            t_i = time.clock()
            terrain.afficher()
            robot.afficher()
            pygame.display.flip()
            if choix == "tout droit":
                if choix2 == "droite":
                    robot.vg = v * 100
                    robot.vd = - (robot.vg * (robot.l - robot.d)) / (2 * robot.l)
                elif choix2 == "gauche":
                    robot.vd = v * 100
                    robot.vg = - (robot.vd * (robot.l - robot.d)) / (2 * robot.l)
            else:
                robot.vd = 0
                robot.vg = v * 100
            robot.mouvement(time.clock() - t_i)
        print("fin")

    else:
        robot.vg = v
        robot.vd = v

    robot.mouvement(time.clock() - t_i)

pygame.quit()