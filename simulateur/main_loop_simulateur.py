# Author: Giraudo Anthony                     
# 23 mars 2018
# main_loop_simulateur.py

import pygame
from pygame.locals import *
pygame.init()
from fonctions import *
from classes import *

#"champi.png", "r2d2.jpg", (75, 75), (49, 49), 200, 55, 50, 75
#def __init__(self, image_roue, image_capteur, dimensions_image_roue, dimensions_image_capteur, l, d, r, z, vitesse_normale, coeff):

image_roue = "champi.png"
image_capteur = "r2d2.jpg"
dimensions_image_roue = (75, 75)
dimensions_image_capteur = (49, 49)

largeur_route = 40

l = 4 * largeur_route # distance entre les deux roues en pixels
d = (11 * largeur_route) // 10 # distance entre les capteurs gauche droite en pixels
r = largeur_route # distance entre milieu entre les roues et milieu entre les capteurs gauche droite en pixels
z = (3 * largeur_route) // 2 # distance entre milieu entre les deux roues et capteur central, en pixel

coeff = 100
vitesse_de_marche = pixel(0.2)
choix_1 = "tout droit"
choix_2 = "droite"

robot = Robot(image_roue, image_capteur, dimensions_image_roue, dimensions_image_capteur, l, d, r, z, vitesse_de_marche, coeff)

robot.placer(0, 500)
robot.rotation(3 * 90)
robot.roue_gauche.image.set_colorkey((0,0,0))
robot.roue_droite.image.set_colorkey((0,0,0))
robot.capteur_droit.image.set_colorkey((255, 255, 255))
robot.capteur_gauche.image.set_colorkey((255, 255, 255))
robot.capteur_centre.image.set_colorkey((255, 255, 255))

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

    elif robot.capteur_gauche.est_dans_le_noir() and not robot.capteur_droit.est_dans_le_noir():
        robot.tourner_gauche()

    elif robot.capteur_droit.est_dans_le_noir() and not robot.capteur_gauche.est_dans_le_noir():
        robot.tourner_droite()

    elif robot.capteur_gauche.est_dans_le_noir() and robot.capteur_droit.est_dans_le_noir() and robot.capteur_centre.est_dans_le_noir():
        robot.gerer_intersection(choix_1, choix_2)
        if choix_1 == "tout droit":
            t_i = time.clock()

    #elif not robot.capteur_centre.est_dans_le_noir() and not robot.capteur_droit.est_dans_le_noir() and not robot.capteur_gauche.est_dans_le_noir():
    #    robot.demi_tour()
    #    t_i = time.clock()

    else:
        robot.tout_droit()

    fenetre.blit(fond, (0, 0))
    robot.afficher()
    pygame.display.flip()
    robot.mouvement(time.clock() - t_i)

pygame.quit()
