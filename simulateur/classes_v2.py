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
    def __init__(self, image_roue, image_capteur, dimensions_image_roue, dimensions_image_capteur, l, d, r, z, h, i, vitesse_de_marche, coeff, largeur_chemin):
        """
        :param image_roue:
        :param image_capteur:
        :param dimensions_image_roue_droite:
        :param dimensions_image_capteur:
        :param l: distance entre les deux roues en pixels
        :param d: distance entre les capteurs gauche droite en pixels
        :param r: distance entre milieu entre les roues et milieu entre les capteurs interieur gauche et interieur droit en pixels
        :param z: distance entre milieu entre les deux roues et capteur central, en pixels
        :param h: distance entre milieu entre les deux roues et milieu entre les capteurs exterieur droit et exterieur gauche en pixels
        :param i: distance entre les capteurs exterieurs droits et exterieurs gauche en pixels
        :param vitesse_de_marche: vitesse en pixel par seconde lorsque le robot va tout droit
        :param coeff: coefficient multiplicatif pour les methodes tourne_gauche et tourne_droite
        :param largeur_chemin: largeur du chemin en pixels
        """
        self.roue_gauche = Image(image_roue, dimensions_image_roue)
        self.roue_droite = Image(image_roue, dimensions_image_roue)
        self.capteur_interieur_gauche = Capteur(image_capteur, dimensions_image_capteur)
        self.capteur_interieur_droit = Capteur(image_capteur, dimensions_image_capteur)
        self.capteur_centre = Capteur(image_capteur, dimensions_image_capteur)
        self.capteur_exterieur_droit = Capteur(image_capteur, dimensions_image_capteur)
        self.capteur_exterieur_gauche = Capteur(image_capteur, dimensions_image_capteur)
        self.angle = 0 # en degre
        self.coord = self.roue_gauche.image.get_rect() #fallait bien prendre une image
        self.coord.x = 0
        self.coord.y = 0
        self.coord_exacte_x = 0
        self.coord_exacte_y = 0
        self.l = l #pixels
        self.d = d #pixels
        self.z = z
        self.r = r
        self.h = h
        self.i = i
        self.vitesse_droite = 0 #en pixels par seconde
        self.vitesse_gauche = 0 #en pixels par seconde
        self.vitesse = vitesse_de_marche
        self.coeff = coeff
        self.largeur_chemin = largeur_chemin

    def placer(self, x, y):
        self.coord.x = x
        self.coord.y = y
        self.coord_exacte_x = x
        self.coord_exacte_y = y
        self.roue_droite.placer_centre(int(x + self.l/2 * cos(radian(self.angle))), int(y - self.l/2 * sin(radian(self.angle)))) # repere classique
        self.roue_gauche.placer_centre(int(x - self.l/2 * cos(radian(self.angle))), int(y + self.l/2 * sin(radian(self.angle)))) # repere classique comme dans toute la suite
        self.capteur_interieur_droit.placer_centre(int(x + self.d/2 * cos(radian(self.angle)) - self.r * sin(radian(self.angle))), int(y - self.d/2 * sin(radian(self.angle)) - self.r * cos(radian(self.angle))))
        self.capteur_interieur_gauche.placer_centre(int(x - self.d/2 * cos(radian(self.angle)) - self.r * sin(radian(self.angle))), int(y + self.d/2 * sin(radian(self.angle)) - self.r * cos(radian(self.angle))))
        self.capteur_centre.placer_centre(int(x - self.z * sin(radian(self.angle))), int(y - self.z * cos(radian(self.angle))))
        self.capteur_exterieur_droit.placer_centre(
            int(x + self.i / 2 * cos(radian(self.angle)) - self.h * sin(radian(self.angle))),
            int(y - self.i / 2 * sin(radian(self.angle)) - self.h * cos(radian(self.angle))))
        self.capteur_exterieur_gauche.placer_centre(
            int(x - self.i / 2 * cos(radian(self.angle)) - self.h * sin(radian(self.angle))),
            int(y + self.i / 2 * sin(radian(self.angle)) - self.h * cos(radian(self.angle))))

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
        self.capteur_interieur_droit.deplacer(x, y)
        self.capteur_interieur_gauche.deplacer(x, y)
        self.capteur_centre.deplacer(x, y)
        self.capteur_exterieur_droit.deplacer(x, y)
        self.capteur_exterieur_gauche.deplacer(x, y)

    def afficher(self):
        self.roue_gauche.afficher()
        self.roue_droite.afficher()
        self.capteur_interieur_droit.afficher()
        self.capteur_interieur_gauche.afficher()
        self.capteur_centre.afficher()
        self.capteur_exterieur_droit.afficher()
        self.capteur_exterieur_gauche.afficher()

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
        self.capteur_interieur_droit.placer_centre(int(x + self.d / 2 * cos(radian(self.angle)) - self.r * sin(radian(self.angle))),
                                     int(y - self.d / 2 * sin(radian(self.angle)) - self.r * cos(radian(self.angle))))
        self.capteur_interieur_gauche.placer_centre(int(x - self.d / 2 * cos(radian(self.angle)) - self.r * sin(radian(self.angle))),
                                     int(y + self.d / 2 * sin(radian(self.angle)) - self.r * cos(radian(self.angle))))
        self.capteur_centre.placer_centre(int(x - self.z * sin(radian(self.angle))), int(y - self.z * cos(radian(self.angle))))
        self.capteur_exterieur_droit.placer_centre(
            int(x + self.i / 2 * cos(radian(self.angle)) - self.h * sin(radian(self.angle))),
            int(y - self.i / 2 * sin(radian(self.angle)) - self.h * cos(radian(self.angle))))
        self.capteur_exterieur_gauche.placer_centre(
            int(x - self.i / 2 * cos(radian(self.angle)) - self.h * sin(radian(self.angle))),
            int(y + self.i / 2 * sin(radian(self.angle)) - self.h * cos(radian(self.angle))))

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
            self.capteur_interieur_droit.placer_centre(
                int(self.coord_exacte_x + self.d / 2 * cos(radian(self.angle)) - self.r * sin(radian(self.angle))),
                int(self.coord_exacte_y - self.d / 2 * sin(radian(self.angle)) - self.r * cos(radian(self.angle))))
            self.capteur_interieur_gauche.placer_centre(
                int(self.coord_exacte_x - self.d / 2 * cos(radian(self.angle)) - self.r * sin(radian(self.angle))),
                int(self.coord_exacte_y + self.d / 2 * sin(radian(self.angle)) - self.r * cos(radian(self.angle))))
            self.capteur_centre.placer_centre(
                int(self.coord_exacte_x - self.z * sin(radian(self.angle))),
                int(self.coord_exacte_y - self.z * cos(radian(self.angle))))
            self.capteur_exterieur_droit.placer_centre(
                int(self.coord_exacte_x + self.i / 2 * cos(radian(self.angle)) - self.h * sin(radian(self.angle))),
                int(self.coord_exacte_y - self.i / 2 * sin(radian(self.angle)) - self.h * cos(radian(self.angle))))
            self.capteur_exterieur_gauche.placer_centre(
                int(self.coord_exacte_x - self.i / 2 * cos(radian(self.angle)) - self.h * sin(radian(self.angle))),
                int(self.coord_exacte_y + self.i / 2 * sin(radian(self.angle)) - self.h * cos(radian(self.angle))))

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
            self.capteur_interieur_droit.placer_centre(
                int(self.coord_exacte_x + self.d / 2 * cos(radian(self.angle)) - self.r * sin(radian(self.angle))),
                int(self.coord_exacte_y - self.d / 2 * sin(radian(self.angle)) - self.r * cos(radian(self.angle))))
            self.capteur_interieur_gauche.placer_centre(
                int(self.coord_exacte_x - self.d / 2 * cos(radian(self.angle)) - self.r * sin(radian(self.angle))),
                int(self.coord_exacte_y + self.d / 2 * sin(radian(self.angle)) - self.r * cos(radian(self.angle))))
            self.capteur_centre.placer_centre(
                int(self.coord_exacte_x - self.z * sin(radian(self.angle))),
                int(self.coord_exacte_y - self.z * cos(radian(self.angle))))
            self.capteur_exterieur_droit.placer_centre(
                int(self.coord_exacte_x + self.i / 2 * cos(radian(self.angle)) - self.h * sin(radian(self.angle))),
                int(self.coord_exacte_y - self.i / 2 * sin(radian(self.angle)) - self.h * cos(radian(self.angle))))
            self.capteur_exterieur_gauche.placer_centre(
                int(self.coord_exacte_x - self.i / 2 * cos(radian(self.angle)) - self.h * sin(radian(self.angle))),
                int(self.coord_exacte_y + self.i / 2 * sin(radian(self.angle)) - self.h * cos(radian(self.angle))))

    def controle_moteur(self, vitesse_gauche, vitesse_droite):
        self.vitesse_gauche = vitesse_gauche
        self.vitesse_droite = vitesse_droite

    def tourner_gauche(self):
        K = 2 * self.largeur_chemin
        self.controle_moteur(self.vitesse * self.coeff * (2 * K - self.l) / (
            2 * K + self.l), self.vitesse * self.coeff)

    def tourner_droite(self):
        K = 2 * self.largeur_chemin
        self.controle_moteur(self.vitesse * self.coeff,
                             self.vitesse * self.coeff * (2 * K - self.l) / (
                                 2 * K + self.l))
        
    def demi_tour(self):
        self.controle_moteur(self.vitesse * self.coeff, -self.vitesse * self.coeff)
        while not self.capteur_centre.est_dans_le_noir():
            t_i = time.clock()
            fenetre.blit(fond, (0, 0))
            self.afficher()
            pygame.display.flip()
            self.mouvement(time.clock() - t_i)

    def gerer_intersection(self, choix):
        K = 102/109 * self.largeur_chemin
        if choix == "droite":
            self.controle_moteur(self.vitesse * self.coeff,
                                 self.vitesse * self.coeff * (2 * K - self.l) / (
                                 2 * K + self.l))
        elif choix == "gauche":
            self.controle_moteur(self.vitesse * self.coeff * (2 * K - self.l) / (
                                 2 * K + self.l), self.vitesse * self.coeff)
        elif choix == "tout droit":
            self.controle_moteur(self.vitesse, self.vitesse)

    def tout_droit(self):
        self.controle_moteur(self.vitesse, self.vitesse)

    def stop(self):
        self.controle_moteur(0, 0)
