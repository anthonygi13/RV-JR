# Author: Giraudo Anthony, Kari Hichma, Mac Donald Kilian, Marhino Louise
# 19 février 2018
# classes.py

import pygame
from pygame.locals import *
pygame.init()
from math import cos
from math import sin
from fonctions import *

fenetre = pygame.display.set_mode((1800, 1000))

class Image():
    global fenetre
    def __init__(self, image, dimensions):
        self.image = pygame.image.load(image).convert()
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


class Robot():
    """robot avec deux capteurs"""
    global fenetre
    def __init__(self, image_roue, image_capteur, dimensions_image_roue, dimensions_image_capteur, l, d, r, z):
        """
        :param image_roue:
        :param image_capteur:
        :param dimensions_image_roue_d:
        :param dimensions_image_capteur:
        :param l: distance entre les deux roues en pixels
        :param d: distance entre les capteurs gauche droite en pixels
        :param r: distance entre milieu entre les roues et milieu entre les capteurs gauche droite en pixels
        :param z: distance entre milieu entre les deux roues et capteur central, en pixel
        """
        self.roue_g = Image(image_roue, dimensions_image_roue)
        self.roue_d = Image(image_roue, dimensions_image_roue)
        self.capteur_g = Image(image_capteur, dimensions_image_capteur)
        self.capteur_d = Image(image_capteur, dimensions_image_capteur)
        self.capteur_c = Image(image_capteur, dimensions_image_capteur)
        self.angle = 0 # en degré
        self.coord = self.roue_g.image.get_rect() #fallait bien prendre une image
        self.coord.x = 0
        self.coord.y = 0
        self.coord_exacte_x = 0
        self.coord_exacte_y = 0
        self.l = l #pixels
        self.d = d #pixels
        self.z = z
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
        self.capteur_c.placer_centre(int(x - self.z * sin(radian(self.angle))), int(y - self.z * cos(radian(self.angle))))

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
        self.capteur_c.deplacer(x, y)

    def afficher(self):
        self.roue_g.afficher()
        self.roue_d.afficher()
        self.capteur_d.afficher()
        self.capteur_g.afficher()
        self.capteur_c.afficher()

    def rotation(self, angle):
        """
        :param angle:
        :return:
        ne pas utiliser robot.placer pour avoir l utilite de coord_exacte
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
        self.capteur_c.placer_centre(int(x - self.z * sin(radian(self.angle))), int(y - self.z * cos(radian(self.angle))))

    def mouvement(self, t):
        """
        :return:
        mouvement pendant t secondes avec les equations du mouvement avec va et vb constants
        e_x et e_y orientés comme dans un repere classique != repere pygame
        ne pas utiliser la fonction deplacer dans cette methode, pour pouvoir utiliser coord_exacte
        ne pas non plus utiliser robot.placer
        """

        if self.vd == self.vg:
            self.coord_exacte_x += -sin(radian(self.angle)) * self.vd * t
            self.coord_exacte_y += -cos(radian(self.angle)) * self.vg * t

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
            self.capteur_c.placer_centre(
                int(self.coord_exacte_x - self.z * sin(radian(self.angle))),
                int(self.coord_exacte_y - self.z * cos(radian(self.angle))))

        else:
            angle_initial = self.angle
            self.rotation((self.vd - self.vg) * t / self.l)

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
            self.capteur_c.placer_centre(
                int(self.coord_exacte_x - self.z * sin(radian(self.angle))),
                int(self.coord_exacte_y - self.z * cos(radian(self.angle))))


class Chemin_ellipse():
    def __init__(self, a, b, e):
        # pas de controle sur l image, on utilise forcement cercle.jpg
        self.ellipse_interieure = Image("cercle.jpg", (2*a, 2*b))
        #self.ellipse_interieure.image.set_colorkey((255, 255, 255))
        self.ellipse_interieure.image = pygame.transform.scale(self.ellipse_interieure.image, (2*a, 2*b))
        self.ellipse_interieure.image.set_colorkey((255, 255, 255))
        self.ellipse_exterieure = Image("cercle.jpg", (2*a + e, 2*b + e))
        #self.ellipse_exterieure.image.set_colorkey((255, 255, 255))
        self.ellipse_exterieure.image = pygame.transform.scale(self.ellipse_exterieure.image, (2*a + e, 2*b + e))
        self.ellipse_exterieure.image.set_colorkey((255, 255, 255))
        self.a = a
        self.b = b
        self.e = e
        self.coord_centre = self.ellipse_interieure.image.get_rect()
    def placer_centre(self, x, y):
        self.ellipse_interieure.placer_centre(x, y)
        self.ellipse_exterieure.placer_centre(x, y)
        self.coord_centre.x = x
        self.coord_centre.y = y
    def afficher(self):
        self.ellipse_interieure.afficher()
        self.ellipse_exterieure.afficher()

class Chemin_rectangle():
    def __init__(self, taille_x, taille_y):
        self.rectangle = Image("chemin.jpg", (taille_x, taille_y))
        self.rectangle.image = pygame.transform.scale(self.rectangle.image, (taille_x, taille_y))
        self.coord = self.rectangle.coord
        self.taille_x = taille_x
        self.taille_y = taille_y
    def placer(self, x, y):
        self.rectangle.placer(x, y)
        self.coord.x = x
        self.coord.y = y
    def afficher(self):
        self.rectangle.afficher()

class Terrain():
    global fenetre
    def __init__(self, fond):
        self.rectangles = []
        self.ellipses = []
        self.fond = pygame.image.load(fond)
    def ajouter_rectangle(self, dimensions, x, y):
        # gerer les rectangles comme les ellipses par redimension d image (eventuellement creer une nouvelle classe)
        self.rectangles.append(Chemin_rectangle(dimensions[0], dimensions[1]))
        self.rectangles[-1].placer(x, y)
    def ajouter_ellipse(self, a, b, e, x_centre, y_centre):
        """
        :param a: demi axe horizontal de l ellipise interieure
        :param b: demi axe vertical de l ellipse interieure
        :param e: largeur du chemin
        :return:
        """
        self.ellipses.append(Chemin_ellipse(a, b, e))
        self.ellipses[-1].placer_centre(x_centre, y_centre)
    def signal(self, capteur):
        for chemin in self.rectangles:
            if chemin.coord.x <= capteur.coord_centre.x and capteur.coord_centre.x <= chemin.coord.x + chemin.taille_x and chemin.coord.y <= capteur.coord_centre.y and capteur.coord_centre.y <= chemin.coord.y + chemin.taille_y:
                return True
        for ellipse in self.ellipses:
            if (capteur.coord_centre.x - ellipse.coord_centre.x)**2 / ellipse.a**2 + (capteur.coord_centre.y - ellipse.coord_centre.y)**2 / ellipse.b**2 >= 1 and (capteur.coord_centre.x - ellipse.coord_centre.x)**2 / (ellipse.a + ellipse.e)**2 + (capteur.coord_centre.y - ellipse.coord_centre.y)**2 / (ellipse.b + ellipse.e)**2 <= 1:
                return True
        return False
    def afficher(self):
        fenetre.blit(self.fond, (0, 0))
        for rectangle in self.rectangles:
            rectangle.afficher()
        for ellipse in self.ellipses:
            ellipse.afficher()