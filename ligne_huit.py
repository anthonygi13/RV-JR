from ligne_courbe.py import *

def ligne_intersection(capteurG, capteurD, capteurC, Vg, Vd, Choix):
    while True:
        SuivreLigneDroite(capteurD, capteurG, Vd, Vg)
        if 