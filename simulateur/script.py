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
terrain.ajouter_chemin("chemin.jpg", (1600, 33), 200, 500 - int(33/2))

robot = Robot("champi.png", "r2d2.jpg", (75, 75), (49, 49), 200, 100, 75)


robot.placer(0, 500)
robot.rotation(3 * 90)

v = pixel(0.2)
k = 20


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
        if event.key == K_m:
            robot.rotation(10)

    elif not terrain.signal(robot.capteur_d) and not terrain.signal(robot.capteur_g):
        robot.vg = v
        robot.vd = v

    elif terrain.signal(robot.capteur_d) and not terrain.signal(robot.capteur_g):
        robot.vg = v * 100
        robot.vd = 0

    elif terrain.signal(robot.capteur_g) and not terrain.signal(robot.capteur_d):
        robot.vd = v * 100
        robot.vg = 0

    robot.mouvement(time.clock() - t_i)

pygame.quit()