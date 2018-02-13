# Author: Giraudo Anthony, Kari Hichma, Mac Donald Kilian, Marhino Louise
# 11 février 2018
# simulateur.py

import pygame
from pygame.locals import *
pygame.init()
from math import cos
from math import sin
from math import pi
import time

def radian(angle):
    return (angle / 360) * 2 * pi

def metre(pixels):
    """
    :param pixels: nombre de pixels a convertir
    :return: conversion des pixels en m (echelle de 15 cm pour 100 pixels)
    """
    return pixels / 100 * 0.15

def pixel(metres):
    """
    :param metres: nombre de metres a convertir
    :return: conversions des metres en pixels (echelle de 15 cm pour 100 pixels)
    """
    return metres / 0.15 * 100

class Image():
    global fenetre
    def __init__(self, image, dimensions):
        self.image = pygame.image.load(image)
        self.dimensions = dimensions
        self.coord = self.image.get_rect()
        self.coord_centre = self.image.get_rect().move(int(dimensions[0]/2), int(dimensions[1]/2))
    def placer(self, x, y):
        self.coord.x = x
        self.coord.y = y
        self.coord_centre = self.coord.move(int(self.dimensions[0] / 2), int(self.dimensions[1] / 2))
    def deplacer(self, x, y):
        self.coord = self.coord.move(x, y)
        self.coord_centre = self.coord_centre.move(x, y)
    def placer_centre(self, x, y):
        self.coord.x = x - int(self.dimensions[0] / 2)
        self.coord.y = y - int(self.dimensions[1] / 2)
        self.coord_centre = self.coord.move(int(self.dimensions[0] / 2), int(self.dimensions[1] / 2))
    def afficher(self):
        fenetre.blit(self.image, self.coord)


class Robot(Image):
    global fenetre
    """centre de l'image = centre des roues
    les roues sont de part et d autre du centre (l = dimensions[0])"""
    def __init__(self, image, dimensions):
        Image.__init__(self, image, dimensions)
        self.vd = 0 # en m par secondes
        self.vg = 0 # en m par secondes
        self.angle = 0 # en degré
        self.l = self.dimensions[0]
    def rotation(self, angle):
        self.angle += angle
        #self.image = pygame.transform.rotate(self.image, angle) #a tester : est ce que ça rotate de angle ou est ce que ça rotate de telle sorte a avoir angle ?
    def mouvement(self):
        """mouvement pendant une seconde avec les equations du mouvement avec va et vb constants, e_x et e_y orientés comme dans un repere classique != repere pygame"""
        #pas oublier le cas ou phi point vaut 0
        if self.vd == self.vg:
            self.deplacer(-sin(radian(self.angle)) * self.vd, -cos(radian(self.angle)) * self.vg)
        else:
            self.rotation((self.vd - self.vg) / self.l)
            self.placer_centre(1000 + ((self.vd + self.vg)/(2 * (self.vd - self.vg)/self.l))*cos(radian(self.angle)) - ((self.vd + self.vg)/(2 * (self.vd - self.vg)/self.l)),
                               500 -(((self.vd + self.vg)/(2 * (self.vd - self.vg)/self.l))*sin(radian(self.angle))))


class Robot2():
    """robot avec deux capteurs"""
    global fenetre
    def __init__(self, image_roue, image_capteur, dimensions_image_roue, dimensions_image_capteur, l, d, r):
        """
        :param image_roue:
        :param image_capteur:
        :param dimensions_image_roue_d:
        :param dimensions_image_capteur:
        :param l: distance entre les deux roues en pixels
        :param d: distance entre les deux capteurs en pixels
        :param r: distance entre milieu entre les roues et milieu entre les capteurs en pixels
        """
        self.roue_g = Image(image_roue, dimensions_image_roue)
        self.roue_d = Image(image_roue, dimensions_image_roue)
        self.capteur_g = Image(image_capteur, dimensions_image_capteur)
        self.capteur_d = Image(image_capteur, dimensions_image_capteur)
        self.angle = 0 # en degré
        self.coord = self.roue_g.image.get_rect() #fallait bien prendre une image
        self.coord.x = 0
        self.coord.y = 0
        self.coord_exacte_x = 0
        self.coord_exacte_y = 0
        self.l = l #pixels
        self.d = d #pixels
        self.r = r
        self.vd = 0 #en pixels par seconde
        self.vg = 0 #en pixels par seconde

    def placer(self, x, y):
        self.coord.x = x
        self.coord.y = y
        self.coord_exacte_x = x
        self.coord_exacte_y = y
        self.roue_d.placer_centre(int(x + self.l/2 * cos(radian(self.angle))), int(y - self.l/2 * sin(radian(self.angle)))) # repere classique
        self.roue_g.placer_centre(int(x - self.l/2 * cos(radian(self.angle))), int(y + self.l/2 * sin(radian(self.angle)))) # repere classique comme dans toute la suite
        self.capteur_d.placer_centre(int(x + self.d/2 * cos(radian(self.angle)) - self.r * sin(radian(self.angle))), int(y - self.d/2 * sin(radian(self.angle)) - self.r * cos(radian(self.angle))))
        self.capteur_g.placer_centre(int(x - self.d/2 * cos(radian(self.angle)) - self.r * sin(radian(self.angle))), int(y + self.d/2 * sin(radian(self.angle)) - self.r * cos(radian(self.angle))))

    def deplacer(self, x, y):
        """
        :param x:
        :param y:
        :return:
        necessite d avoir ete place au prealable
        """
        self.coord = self.coord.move(x, y)
        self.coord_exacte_x += x
        self.coord_exacte_y += y
        self.roue_d.deplacer(x, y)
        self.roue_g.deplacer(x, y)
        self.capteur_d.deplacer(x, y)
        self.capteur_g.deplacer(x, y)

    def afficher(self):
        self.roue_g.afficher()
        self.roue_d.afficher()
        self.capteur_d.afficher()
        self.capteur_g.afficher()

    def rotation(self, angle):
        """
        :param angle:
        :return:
        ne pas utiliser placer pour avoir l utilite de coord_exacte
        """
        self.angle += angle
        x = self.coord.x
        y = self.coord.y
        self.roue_d.placer_centre(int(x + self.l / 2 * cos(radian(self.angle))),
                                  int(y - self.l / 2 * sin(radian(self.angle))))
        self.roue_g.placer_centre(int(x - self.l / 2 * cos(radian(self.angle))), int(
            y + self.l / 2 * sin(radian(self.angle))))
        self.capteur_d.placer_centre(int(x + self.d / 2 * cos(radian(self.angle)) - self.r * sin(radian(self.angle))),
                                     int(y - self.d / 2 * sin(radian(self.angle)) - self.r * cos(radian(self.angle))))
        self.capteur_g.placer_centre(int(x - self.d / 2 * cos(radian(self.angle)) - self.r * sin(radian(self.angle))),
                                     int(y + self.d / 2 * sin(radian(self.angle)) - self.r * cos(radian(self.angle))))

    def mouvement(self):
        """
        :return:
        mouvement pendant une seconde avec les equations du mouvement avec va et vb constants
        e_x et e_y orientés comme dans un repere classique != repere pygame
        prb : quand vitesse d'une roue vaut 0, elle se deplace quand meme... c normal, probleme c que les pixels c discret
        ne pas utiliser les fonctions deplacer et placer dans cette methode, pour pouvoir utiliser coord_exacte
        """

        if self.vd == self.vg:
            x = int(-sin(radian(self.angle)) * self.vd)
            y = int(-cos(radian(self.angle)) * self.vg)
            self.coord = self.coord.move(x, y)
            self.roue_d.deplacer(x, y)
            self.roue_g.deplacer(x, y)
            self.capteur_d.deplacer(x, y)
            self.capteur_g.deplacer(x, y)

            self.coord_exacte_x += -sin(radian(self.angle)) * self.vd
            self.coord_exacte_y += -cos(radian(self.angle)) * self.vg

        else:
            angle_initial = self.angle
            self.rotation((self.vd - self.vg) / self.l)

            self.coord_exacte_x += ((self.vd + self.vg) / (2 * (self.vd - self.vg) / self.l)) * cos(
                radian(self.angle)) - (
                                          (self.vd + self.vg) / (2 * (self.vd - self.vg) / self.l)) * cos(
                radian(angle_initial))
            self.coord_exacte_y += -(
            ((self.vd + self.vg) / (2 * (self.vd - self.vg) / self.l)) * sin(radian(self.angle))) \
                                   + (self.vd + self.vg) / (2 * (self.vd - self.vg) / self.l) * sin(
                radian(angle_initial))

            self.coord.x = int(self.coord_exacte_x)
            self.coord.y = int(self.coord_exacte_y)

            self.roue_d.placer_centre(int(self.coord_exacte_x + self.l / 2 * cos(radian(self.angle))),
                                      int(self.coord_exacte_y - self.l / 2 * sin(radian(self.angle))))
            self.roue_g.placer_centre(int(self.coord_exacte_x - self.l / 2 * cos(radian(self.angle))), int(
                self.coord_exacte_y + self.l / 2 * sin(radian(self.angle))))
            self.capteur_d.placer_centre(
                int(self.coord_exacte_x + self.d / 2 * cos(radian(self.angle)) - self.r * sin(radian(self.angle))),
                int(self.coord_exacte_y - self.d / 2 * sin(radian(self.angle)) - self.r * cos(radian(self.angle))))
            self.capteur_g.placer_centre(
                int(self.coord_exacte_x - self.d / 2 * cos(radian(self.angle)) - self.r * sin(radian(self.angle))),
                int(self.coord_exacte_y + self.d / 2 * sin(radian(self.angle)) - self.r * cos(radian(self.angle))))


        """
        if self.vd == self.vg:
            self.deplacer(int(-sin(radian(self.angle)) * self.vd), int(-cos(radian(self.angle)) * self.vg))
        else:
            angle_initial = self.angle
            self.rotation((self.vd - self.vg) / self.l)
            self.deplacer(
                int(((self.vd + self.vg) / (2 * (self.vd - self.vg) / self.l)) * cos(radian(self.angle)) - (
                (self.vd + self.vg) / (2 * (self.vd - self.vg) / self.l)) * cos(radian(angle_initial))),
                int(-(((self.vd + self.vg) / (2 * (self.vd - self.vg) / self.l)) * sin(radian(self.angle))) +
                (self.vd + self.vg) / (2 * (self.vd - self.vg) / self.l) * sin(radian(angle_initial))))

            #self.placer(1000 + int(((self.vd + self.vg) / (2 * (self.vd - self.vg) / self.l)) * cos(radian(self.angle)) - (
                (self.vd + self.vg) / (2 * (self.vd - self.vg) / self.l))),
                500 + int(-(((self.vd + self.vg) / (2 * (self.vd - self.vg) / self.l)) * sin(radian(self.angle)))))

            #self.placer(
                1000 + int(((self.vd + self.vg) / (2 * (self.vd - self.vg) / self.l)) * cos(radian(self.angle)) - (
                    (self.vd + self.vg) / (2 * (self.vd - self.vg) / self.l) * cos(radian(45)))),
                500 + int(-(((self.vd + self.vg) / (2 * (self.vd - self.vg) / self.l)) * sin(radian(self.angle)))+
                (self.vd + self.vg) / (2 * (self.vd - self.vg) / self.l) * sin(radian(45))))
        """



fenetre = pygame.display.set_mode((1800, 1000))

fond = pygame.image.load("fond.png")
fenetre.blit(fond, (0, 0))

robot = Robot2("champi.png", "champi.png", (75, 75), (75, 75), 200, 100, 75)

robot.placer(1000, 500)
robot.afficher()

robot.vd = 500
robot.vg = 0

pygame.display.flip()


continuer = True
while continuer == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False


    if event.type == KEYDOWN:
        if event.key == K_m:
            robot.rotation(10)
            fenetre.blit(fond, (0, 0))
            robot.afficher()
            pygame.display.flip()



    robot.mouvement()

    fenetre.blit(fond, (0, 0))
    robot.afficher()
    pygame.display.flip()



pygame.quit()