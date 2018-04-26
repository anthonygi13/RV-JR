# Authors: Anthony Giraudo, Kari Hichma, Kilian Mac Donald, Louise Marinho
# 19 février 2018
# classes_simulateur.py

import pygame
from pygame.locals import *
import time
pygame.init()
from math import cos
from math import sin
from conversions import *

fenetre = pygame.display.set_mode((1800, 1000)) # fenetre utilisee en tant que variable globale
fond = pygame.image.load("terrain.png") # image d un chemin noir sur fond blanc, utilisee en tant que variable globale

class Image(): # classe permettant de manipuler plus aisement les images a afficher a l ecran

    global fenetre

    def __init__(self, image, dimensions):
        """
        :param image: chemin vers une image rectangulaire
        :param dimensions: tuple de la forme (x, y) avec x la largeur de l image et y sa hauteur
        """

        self.image = pygame.image.load(image).convert()
        self.dimensions = dimensions
        self.coord = self.image.get_rect() # coordonnees dans la fenetre du point le plus en haut a gauche de l image
        self.coord_centre = self.image.get_rect().move(int(dimensions[0]/2), int(dimensions[1]/2)) # coordonnees dans la fenetre du point au centre de l image

    def placer(self, x, y): # place l image a un autre endroit de la fenetre
        """
        :param x: nouvelles coordonnees en x du point le plus en haut a gauche de l image
        :param y: nouvelles coordonnees en y du point le plus en haut a gauche de l image
        """

        self.coord.x = x
        self.coord.y = y
        self.coord_centre = self.coord.move(int(self.dimensions[0] / 2), int(self.dimensions[1] / 2))

    def placer_centre(self, x, y): # place l image a un autre endroit de la fenetre
        """
        :param x: nouvelles coordonnees en x du point au centre de l image
        :param y: nouvelles coordonnees en y du point au centre de l image
        """

        self.coord.x = x - int(self.dimensions[0] / 2)
        self.coord.y = y - int(self.dimensions[1] / 2)
        self.coord_centre = self.coord.move(int(self.dimensions[0] / 2), int(self.dimensions[1] / 2))

    def afficher(self): # affiche l image dans la fenetre

        fenetre.blit(self.image, self.coord)


class Capteur(Image): # classe pour gerer les images representant les capteurs

    global fenetre
    global fond

    def __init__(self, image, dimensions):
        """
        :param image: chemin vers une image rectangulaire
        :param dimensions: tuple de la forme (x, y) avec x la largeur de l image et y sa hauteur
        """

        Image.__init__(self, image, dimensions)

    def est_dans_le_noir(self): # permet de savoir si le capteur detecte du noir ou pas
        """
        :return: True si le centre du capteur n est pas a l emplacement d un pixel ayant comme valeur 255 pour r, g ou b
         et False sinon.
         On suppose que le fond est un chemin noir sur fond blanc avec un chemin noir
        """

        rgb = tuple(fond.get_at((self.coord_centre.x, self.coord_centre.y)))
        for i in range(3):
            if rgb[i] == 255:
                return False
        return True


class Robot(): # classe permettant de gerer la simulation du comportement du robot, qui est forme de 7 images : 5 capteurs et 2 roues

    global fenetre
    global fond

    def __init__(self, image_roue, image_capteur, dimensions_image_roue, dimensions_image_capteur, l, d, r, z, h, i, vitesse_de_marche, coeff, largeur_chemin):
        """
        :param image_roue: chemin vers une image representant une roue
        :param image_capteur: chemin vers une image representant un capteur
        :param dimensions_image_roue: tuple de la forme (x, y) avec x la largeur de l image representant une roue et y sa hauteur
        :param dimensions_image_capteur: tuple de la forme (x, y) avec x la largeur de l image representant un capteur et y sa hauteur
        :param l: distance entre les deux roues en pixels
        :param d: distance entre les capteurs gauche droite en pixels
        :param r: distance entre milieu entre les roues et milieu entre les capteurs interieur gauche et interieur droit en pixels
        :param z: distance entre milieu entre les deux roues et capteur central, en pixels
        :param h: distance entre milieu entre les deux roues et milieu entre les capteurs exterieur droit et exterieur gauche en pixels
        :param i: distance entre les capteurs exterieurs droits et exterieurs gauche en pixels
        :param vitesse_de_marche: vitesse en pixel par seconde lorsque le robot va tout droit
        :param coeff: coefficient multiplicatif pour les methodes tourner_gauche et tourner_droite et gerer_intersection
        :param largeur_chemin: largeur du chemin en pixels
        """

        self.roue_gauche = Image(image_roue, dimensions_image_roue)
        self.roue_droite = Image(image_roue, dimensions_image_roue)
        self.capteur_interieur_gauche = Capteur(image_capteur, dimensions_image_capteur)
        self.capteur_interieur_droit = Capteur(image_capteur, dimensions_image_capteur)
        self.capteur_centre = Capteur(image_capteur, dimensions_image_capteur)
        self.capteur_exterieur_droit = Capteur(image_capteur, dimensions_image_capteur)
        self.capteur_exterieur_gauche = Capteur(image_capteur, dimensions_image_capteur)
        self.angle = 0 # en degre, l'angle oriente entre l horizontale de gauche a droite et le vecteur reliant les deux roues de la roue gauche a la roue droite
        # les coordonnees du robot sont les coordonnees du point a equidistance des deux roues
        # sur l axe forme par les centres des images correspondant aux roues
        self.coord = pygame.Rect((0, 0), (0, 0))
        self.coord_exacte_x = 0 # stocke dans une variable floattante la coordonnee en x theorique du robot
        self.coord_exacte_y = 0 # stocke dans une variable floattante la coordonnee en y theorique du robot
        self.l = l
        self.d = d
        self.z = z
        self.r = r
        self.h = h
        self.i = i
        self.vitesse_droite = 0 #en pixels par seconde
        self.vitesse_gauche = 0 #en pixels par seconde
        self.vitesse = vitesse_de_marche # vitesse en pixels par seconde lorsque le robot va tout droit
        self.coeff = coeff
        self.largeur_chemin = largeur_chemin

    def afficher(self): # affiche les images representant le robot

        self.roue_gauche.afficher()
        self.roue_droite.afficher()
        self.capteur_interieur_droit.afficher()
        self.capteur_interieur_gauche.afficher()
        self.capteur_centre.afficher()
        self.capteur_exterieur_droit.afficher()
        self.capteur_exterieur_gauche.afficher()

    def placer(self, x, y): # place les images representant le robot a un autre endroit de la fenetre
        """
        :param x: nouvelles coordonnees en x du robot
        :param y: nouvelles coordonnees en y du robot
        """

        self.coord.x = x
        self.coord.y = y
        self.coord_exacte_x = x
        self.coord_exacte_y = y
        self.roue_droite.placer_centre(int(x + self.l / 2 * cos(radian(self.angle))),
                                        int(y - self.l / 2 * sin(radian(self.angle))))  # repere classique
        self.roue_gauche.placer_centre(int(x - self.l / 2 * cos(radian(self.angle))), int(
            y + self.l / 2 * sin(radian(self.angle))))  # repere classique comme dans toute la suite
        self.capteur_interieur_droit.placer_centre(
            int(x + self.d / 2 * cos(radian(self.angle)) - self.r * sin(radian(self.angle))),
            int(y - self.d / 2 * sin(radian(self.angle)) - self.r * cos(radian(self.angle))))
        self.capteur_interieur_gauche.placer_centre(
            int(x - self.d / 2 * cos(radian(self.angle)) - self.r * sin(radian(self.angle))),
            int(y + self.d / 2 * sin(radian(self.angle)) - self.r * cos(radian(self.angle))))
        self.capteur_centre.placer_centre(int(x - self.z * sin(radian(self.angle))),
                                            int(y - self.z * cos(radian(self.angle))))
        self.capteur_exterieur_droit.placer_centre(
            +
            int(x + self.i / 2 * cos(radian(self.angle)) - self.h * sin(radian(self.angle))),
            int(y - self.i / 2 * sin(radian(self.angle)) - self.h * cos(radian(self.angle))))
        self.capteur_exterieur_gauche.placer_centre(
            int(x - self.i / 2 * cos(radian(self.angle)) - self.h * sin(radian(self.angle))),
            int(y + self.i / 2 * sin(radian(self.angle)) - self.h * cos(radian(self.angle))))

    def rotation(self, angle): # rotation du robot
        """
        :param angle: valeur en degre de l angle dont on veut faire tourner le robot
        """

        self.angle += angle
        x = self.coord.x
        y = self.coord.y
        self.roue_droite.placer_centre(int(x + self.l / 2 * cos(radian(self.angle))),
                                  int(y - self.l / 2 * sin(radian(self.angle))))
        self.roue_gauche.placer_centre(int(x - self.l / 2 * cos(radian(self.angle))),
                                       int(y + self.l / 2 * sin(radian(self.angle))))
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

    def mouvement(self, t): # simule un deplacement du robot d'une certaine duree en considerant les vitesses des roues constantes
        """
        :param t: duree supposee du deplacement, qui s effectue instantanement
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

    def controle_moteur(self, vitesse_gauche, vitesse_droite): # change les vitesses des roues
        """
        :param vitesse_gauche: nouvelle vitesse de la roue droite en pixels par seconde
        :param vitesse_droite: nouvelle vitesse de la roue gauche en pixels par seconde
        """

        self.vitesse_gauche = vitesse_gauche
        self.vitesse_droite = vitesse_droite

    def tourner_gauche(self): # change les vitesses des roues pour rectifier la trajectoire du robot vers la gauche

        #K = 2 * self.largeur_chemin
        #self.controle_moteur(self.vitesse * self.coeff * (2 * K - self.l) / (2 * K + self.l),
        #                     self.vitesse * self.coeff)

        self.controle_moteur(-self.vitesse * self.coeff, self.vitesse * self.coeff)

    def tourner_droite(self): # change les vitesses des roues pour rectifier la trajectoire du robot vers la droite

        #K = 2 * self.largeur_chemin
        #self.controle_moteur(self.vitesse * self.coeff,
        #                     self.vitesse * self.coeff * (2 * K - self.l) / (2 * K + self.l))

        self.controle_moteur(self.vitesse * self.coeff, -self.vitesse * self.coeff)

    def demi_tour(self): # fait faire un demi tour au robot tant que le capteur central ne detecte pas de noir
        """
        :return: False si la touche d arret de demi tour n a pas ete pressee, False sinon
        """

        self.controle_moteur(self.vitesse * self.coeff, -self.vitesse * self.coeff)
        stop = False
        while not self.capteur_centre.est_dans_le_noir():
            t_i = time.clock()
            fenetre.blit(fond, (0, 0))
            self.afficher()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:  # stopper le robot en cas d appui sur la touche d
                        stop = True
            if stop:
                return True
            else:
                self.mouvement(time.clock() - t_i)
        return False

    def gerer_intersection(self, choix): # change les vitesses des roues pour que le robot aille dans la direction voulue a une intersection
        """
        :param choix: chaine de caracteres correspondant au choix de la direction a prendre a l intersection,
         "droite", "gauche" ou "tout droit"
        """

        if not choix in ["droite", "gauche", "tout droit"]:
            raise ValueError("Le choix n est pas valide")

        K = 1 * self.largeur_chemin

        if choix == "droite":
            self.controle_moteur(self.vitesse * self.coeff,
                                 self.vitesse * self.coeff * (2 * K - self.l) / (2 * K + self.l))

        elif choix == "gauche":
            self.controle_moteur(self.vitesse * self.coeff * (2 * K - self.l) / (2 * K + self.l),
                                 self.vitesse * self.coeff)

        elif choix == "tout droit":
            self.controle_moteur(self.vitesse, self.vitesse)

    def tout_droit(self): # change les vitesses des roues pour que le robot aille tout droit a la vitesse self.vitesse

        self.controle_moteur(self.vitesse, self.vitesse)

    def stop(self): # stoppe le mouvement du robot

        self.controle_moteur(0, 0)

