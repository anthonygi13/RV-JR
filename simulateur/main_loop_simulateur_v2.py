# Author: Giraudo Anthony                     
# 23 mars 2018
# main_loop_simulateur.py

import pygame
from pygame.locals import *
pygame.init()
from conversions import *
from classes_v2 import *
import time

image_roue = "champi.png"
image_capteur = "r2d2.jpg"
dimensions_image_roue = (75, 75)
dimensions_image_capteur = (49, 49)

largeur_chemin = 40

l = 4 * largeur_chemin # distance entre les deux roues en pixels
d = (11 * largeur_chemin) // 10 # distance entre les capteurs gauche droite en pixels
r = largeur_chemin # distance entre milieu entre les roues et milieu entre les capteurs gauche droite en pixels
z = (3 * largeur_chemin) // 2 # distance entre milieu entre les deux roues et capteur central, en pixel
h = 3 * largeur_chemin // 2 + r # distance entre milieu entre les deux roues et milieu entre les capteurs exterieur droit et exterieur gauche en pixels
i = d * 2 # distance entre les capteurs exterieurs droits et exterieurs gauche en pixels

coeff = 100
vitesse_de_marche = pixel(0.01)
choix = "droite"

robot = Robot(image_roue, image_capteur, dimensions_image_roue, dimensions_image_capteur, l, d, r, z, h, i, vitesse_de_marche, coeff, largeur_chemin)

robot.placer(0, 500)
robot.rotation(3 * 90)

# rend le noir transparent
robot.roue_gauche.image.set_colorkey((0,0,0))
robot.roue_droite.image.set_colorkey((0,0,0))
robot.capteur_interieur_droit.image.set_colorkey((255, 255, 255))
robot.capteur_interieur_gauche.image.set_colorkey((255, 255, 255))
robot.capteur_centre.image.set_colorkey((255, 255, 255))
robot.capteur_exterieur_droit.image.set_colorkey((255, 255, 255))
robot.capteur_exterieur_gauche.image.set_colorkey((255, 255, 255))


continuer = True
while continuer:
    t_i = time.clock()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_s:
            robot.controle_moteur(0, 0)
        if event.key == K_m:
            robot.rotation(10)
        if event.key == K_v:
            robot.vitesse = pixel(0.2)
        if event.key == K_r:
            robot.vitesse = vitesse_de_marche

    elif robot.capteur_interieur_gauche.est_dans_le_noir() and not robot.capteur_interieur_droit.est_dans_le_noir():
        robot.tourner_gauche()

    elif robot.capteur_interieur_droit.est_dans_le_noir() and not robot.capteur_interieur_gauche.est_dans_le_noir():
        robot.tourner_droite()

    elif robot.capteur_interieur_gauche.est_dans_le_noir() and robot.capteur_exterieur_gauche.est_dans_le_noir() and\
            robot.capteur_interieur_droit.est_dans_le_noir() and robot.capteur_exterieur_droit.est_dans_le_noir() and robot.capteur_centre.est_dans_le_noir():
        robot.stop()

    elif robot.capteur_interieur_gauche.est_dans_le_noir() and robot.capteur_interieur_droit.est_dans_le_noir() and robot.capteur_centre.est_dans_le_noir():
        robot.gerer_intersection(choix)

    #elif not robot.capteur_centre.est_dans_le_noir() and not robot.capteur_interieur_droit.est_dans_le_noir() and not robot.capteur_interieur_gauche.est_dans_le_noir():
    #    robot.demi_tour()
    #    t_i = time.clock()

    else:
        robot.tout_droit()

    fenetre.blit(fond, (0, 0))
    robot.afficher()
    pygame.display.flip()
    robot.mouvement(time.clock() - t_i)

pygame.quit()
