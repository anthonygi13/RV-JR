# Author: Giraudo Anthony, Kari Hichma, Mac Donald Kilian, Marhino Louise
# 19 février 2018
# classes.py

import pygame
from pygame.locals import *
import time
pygame.init()
from math import cos
from math import sin
from conversions import *

fenetre = pygame.display.set_mode((1800, 1000))
fond = pygame.image.load("terrain.png")

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

class Capteur(Image):
    global fenetre
    global fond
    def __init__(self, image, dimensions):
        Image.__init__(self, image, dimensions)

    def est_dans_le_noir(self):
        rgb = tuple(fond.get_at((self.coord_centre.x, self.coord_centre.y)))
        for i in range(3):
            if rgb[i] == 255: #!=0
                return False
        return True

class Robot():
    """robot avec deux capteurs"""
    global fenetre
    global fond
    def __init__(self, image_roue, image_capteur, dimensions_image_roue, dimensions_image_capteur, l, d, r, z, vitesse_de_marche, coeff):
        """
        :param image_roue:
        :param image_capteur:
        :param dimensions_image_roue_droite:
        :param dimensions_image_capteur:
        :param l: distance entre les deux roues en pixels
        :param d: distance entre les capteurs gauche droite en pixels
        :param r: distance entre milieu entre les roues et milieu entre les capteurs gauche droite en pixels
        :param z: distance entre milieu entre les deux roues et capteur central, en pixel
        """
        self.roue_gauche = Image(image_roue, dimensions_image_roue)
        self.roue_droite = Image(image_roue, dimensions_image_roue)
        self.capteur_gauche = Capteur(image_capteur, dimensions_image_capteur)
        self.capteur_droit = Capteur(image_capteur, dimensions_image_capteur)
        self.capteur_centre = Capteur(image_capteur, dimensions_image_capteur)
        self.angle = 0 # en degré
        self.coord = self.roue_gauche.image.get_rect() #fallait bien prendre une image
        self.coord.x = 0
        self.coord.y = 0
        self.coord_exacte_x = 0
        self.coord_exacte_y = 0
        self.l = l #pixels
        self.d = d #pixels
        self.z = z
        self.r = r
        self.vitesse_droite = 0 #en pixels par seconde
        self.vitesse_gauche = 0 #en pixels par seconde
        self.vitesse = vitesse_de_marche
        self.coeff = coeff

    def placer(self, x, y):
        self.coord.x = x
        self.coord.y = y
        self.coord_exacte_x = x
        self.coord_exacte_y = y
        self.roue_droite.placer_centre(int(x + self.l/2 * cos(radian(self.angle))), int(y - self.l/2 * sin(radian(self.angle)))) # repere classique
        self.roue_gauche.placer_centre(int(x - self.l/2 * cos(radian(self.angle))), int(y + self.l/2 * sin(radian(self.angle)))) # repere classique comme dans toute la suite
        self.capteur_droit.placer_centre(int(x + self.d/2 * cos(radian(self.angle)) - self.r * sin(radian(self.angle))), int(y - self.d/2 * sin(radian(self.angle)) - self.r * cos(radian(self.angle))))
        self.capteur_gauche.placer_centre(int(x - self.d/2 * cos(radian(self.angle)) - self.r * sin(radian(self.angle))), int(y + self.d/2 * sin(radian(self.angle)) - self.r * cos(radian(self.angle))))
        self.capteur_centre.placer_centre(int(x - self.z * sin(radian(self.angle))), int(y - self.z * cos(radian(self.angle))))

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
        self.roue_droite.deplacer(x, y)
        self.roue_gauche.deplacer(x, y)
        self.capteur_droit.deplacer(x, y)
        self.capteur_gauche.deplacer(x, y)
        self.capteur_centre.deplacer(x, y)

    def afficher(self):
        self.roue_gauche.afficher()
        self.roue_droite.afficher()
        self.capteur_droit.afficher()
        self.capteur_gauche.afficher()
        self.capteur_centre.afficher()

    def rotation(self, angle):
        """
        :param angle:
        :return:
        ne pas utiliser robot.placer pour avoir l utilite de coord_exacte
        """
        self.angle += angle
        x = self.coord.x
        y = self.coord.y
        self.roue_droite.placer_centre(int(x + self.l / 2 * cos(radian(self.angle))),
                                  int(y - self.l / 2 * sin(radian(self.angle))))
        self.roue_gauche.placer_centre(int(x - self.l / 2 * cos(radian(self.angle))), int(
            y + self.l / 2 * sin(radian(self.angle))))
        self.capteur_droit.placer_centre(int(x + self.d / 2 * cos(radian(self.angle)) - self.r * sin(radian(self.angle))),
                                     int(y - self.d / 2 * sin(radian(self.angle)) - self.r * cos(radian(self.angle))))
        self.capteur_gauche.placer_centre(int(x - self.d / 2 * cos(radian(self.angle)) - self.r * sin(radian(self.angle))),
                                     int(y + self.d / 2 * sin(radian(self.angle)) - self.r * cos(radian(self.angle))))
        self.capteur_centre.placer_centre(int(x - self.z * sin(radian(self.angle))), int(y - self.z * cos(radian(self.angle))))

    def mouvement(self, t):
        """
        :return:
        mouvement pendant t secondes avec les equations du mouvement avec va et vb constants
        e_x et e_y orientés comme dans un repere classique != repere pygame
        ne pas utiliser la fonction deplacer dans cette methode, pour pouvoir utiliser coord_exacte
        ne pas non plus utiliser robot.placer
        """

        if self.vitesse_droite == self.vitesse_gauche:
            self.coord_exacte_x += -sin(radian(self.angle)) * self.vitesse_droite * t
            self.coord_exacte_y += -cos(radian(self.angle)) * self.vitesse_gauche * t

            self.coord.x = int(self.coord_exacte_x)
            self.coord.y = int(self.coord_exacte_y)

            self.roue_droite.placer_centre(int(self.coord_exacte_x + self.l / 2 * cos(radian(self.angle))),
                                      int(self.coord_exacte_y - self.l / 2 * sin(radian(self.angle))))
            self.roue_gauche.placer_centre(int(self.coord_exacte_x - self.l / 2 * cos(radian(self.angle))), int(
                self.coord_exacte_y + self.l / 2 * sin(radian(self.angle))))
            self.capteur_droit.placer_centre(
                int(self.coord_exacte_x + self.d / 2 * cos(radian(self.angle)) - self.r * sin(radian(self.angle))),
                int(self.coord_exacte_y - self.d / 2 * sin(radian(self.angle)) - self.r * cos(radian(self.angle))))
            self.capteur_gauche.placer_centre(
                int(self.coord_exacte_x - self.d / 2 * cos(radian(self.angle)) - self.r * sin(radian(self.angle))),
                int(self.coord_exacte_y + self.d / 2 * sin(radian(self.angle)) - self.r * cos(radian(self.angle))))
            self.capteur_centre.placer_centre(
                int(self.coord_exacte_x - self.z * sin(radian(self.angle))),
                int(self.coord_exacte_y - self.z * cos(radian(self.angle))))

        else:
            angle_initial = self.angle
            self.rotation((self.vitesse_droite - self.vitesse_gauche) * t / self.l)

            self.coord_exacte_x += ((self.vitesse_droite + self.vitesse_gauche) / (2 * (self.vitesse_droite - self.vitesse_gauche) / self.l)) * cos(
                radian(self.angle)) - (
                                          (self.vitesse_droite + self.vitesse_gauche) / (2 * (self.vitesse_droite - self.vitesse_gauche) / self.l)) * cos(
                radian(angle_initial))
            self.coord_exacte_y += -(
            ((self.vitesse_droite + self.vitesse_gauche) / (2 * (self.vitesse_droite - self.vitesse_gauche) / self.l)) * sin(radian(self.angle))) \
                                   + (self.vitesse_droite + self.vitesse_gauche) / (2 * (self.vitesse_droite - self.vitesse_gauche) / self.l) * sin(
                radian(angle_initial))

            self.coord.x = int(self.coord_exacte_x)
            self.coord.y = int(self.coord_exacte_y)

            self.roue_droite.placer_centre(int(self.coord_exacte_x + self.l / 2 * cos(radian(self.angle))),
                                      int(self.coord_exacte_y - self.l / 2 * sin(radian(self.angle))))
            self.roue_gauche.placer_centre(int(self.coord_exacte_x - self.l / 2 * cos(radian(self.angle))), int(
                self.coord_exacte_y + self.l / 2 * sin(radian(self.angle))))
            self.capteur_droit.placer_centre(
                int(self.coord_exacte_x + self.d / 2 * cos(radian(self.angle)) - self.r * sin(radian(self.angle))),
                int(self.coord_exacte_y - self.d / 2 * sin(radian(self.angle)) - self.r * cos(radian(self.angle))))
            self.capteur_gauche.placer_centre(
                int(self.coord_exacte_x - self.d / 2 * cos(radian(self.angle)) - self.r * sin(radian(self.angle))),
                int(self.coord_exacte_y + self.d / 2 * sin(radian(self.angle)) - self.r * cos(radian(self.angle))))
            self.capteur_centre.placer_centre(
                int(self.coord_exacte_x - self.z * sin(radian(self.angle))),
                int(self.coord_exacte_y - self.z * cos(radian(self.angle))))

    def controle_moteur(self, vitesse_gauche, vitesse_droite):
        self.vitesse_gauche = vitesse_gauche
        self.vitesse_droite = vitesse_droite

    def tourner_gauche(self):
        self.controle_moteur(0, self.vitesse * self.coeff)
    
    def tourner_droite(self):
        self.controle_moteur(self.vitesse * self.coeff, 0)
        
    def demi_tour(self):
        self.controle_moteur(self.vitesse * self.coeff, -self.vitesse * self.coeff)
        while not self.capteur_centre.est_dans_le_noir():
            t_i = time.clock()
            fenetre.blit(fond, (0, 0))
            self.afficher()
            pygame.display.flip()
            self.mouvement(time.clock() - t_i)

    def gerer_intersection(self, choix_1, choix_2=None):
        if choix_1 == "droite":
            self.controle_moteur(self.vitesse * self.coeff, -(self.vitesse * self.coeff * (self.l - self.d) / (2 * self.l))) #(l-d)/2l = 0.3625
        elif choix_1 == "gauche":
            self.controle_moteur(-(self.vitesse * self.coeff * (self.l - self.d) / (2 * self.l)), self.vitesse * self.coeff)
        elif choix_1 == "tout droit":
            assert choix_2 is not None
            self.controle_moteur(self.vitesse, self.vitesse)
            while self.capteur_centre.est_dans_le_noir() and self.capteur_droit.est_dans_le_noir() and self.capteur_gauche.est_dans_le_noir():
                t_i = time.clock()
                fenetre.blit(fond, (0, 0))
                self.afficher()
                pygame.display.flip()
                self.mouvement(time.clock() - t_i)
            if not self.capteur_centre.est_dans_le_noir():
                if choix_2 == "droite":
                    self.controle_moteur(self.vitesse * self.coeff, -(self.vitesse * self.coeff * (self.l - self.d)) / (2 * self.l))
                elif choix_2 == "gauche":
                    self.controle_moteur(-(self.vitesse * self.coeff * (self.l - self.d) / (2 * self.l)), self.vitesse * self.coeff)
                while not self.capteur_centre.est_dans_le_noir():
                    t_i = time.clock()
                    fenetre.blit(fond, (0, 0))
                    self.afficher()
                    pygame.display.flip()
                    self.mouvement(time.clock() - t_i)

    def tout_droit(self):
        self.controle_moteur(self.vitesse, self.vitesse)

    
        
    



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
