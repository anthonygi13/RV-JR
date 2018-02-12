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

fenetre = pygame.display.set_mode((1800, 1000))

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
    #a revoir..., tout
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
        """mouvement pendant une seconde avec les equations du mouvement avec va et vb constants"""
        #pas oublier le cas ou phi point vaut 0
        self.rotation((self.vd - self.vg) / self.l)
        self.placer_centre(1000 + ((self.vd + self.vg)/(2 * (self.vd - self.vg)/self.l))*cos(radian(self.angle)) - ((self.vd + self.vg)/(2 * (self.vd - self.vg)/self.l)), 500 + ((self.vd + self.vg)/(2 * (self.vd - self.vg)/self.l))*sin(radian(self.angle)))


# a faire : convertir metre et pixels, faire une echelle


fond = pygame.image.load("fond.png")

champi = Robot("champi.png", (75, 75))
champi.image.set_colorkey((0,0,0))
champi.vg = 200
champi.vd = 100

fenetre.blit(fond, (0, 0))
champi.placer_centre(1000, 500)
champi.afficher()

pygame.display.flip()



continuer = True
while continuer == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False
    """
    if event.type == KEYDOWN:
        if event.key == K_m:
            champi.rotation(10)
            print(champi.angle)
    """

    champi.mouvement()

    fenetre.blit(fond, (0, 0))
    champi.afficher()
    pygame.display.flip()



pygame.quit()