# Mac Donald  Kilian
# ligne_impasse
# crée le 11/02/2018

from ligne_courbe.py import *

def Impasse (capteurG, capteurC, capteurD, K, Vg, Vd, choix):
	while True:
    	SuivreLigneDroite(capteurD, capteurC, capteurG, K, Vd, Vg)
        if capteurC == 0 :
        	while capteurC !=1:
            	if choix == 'gauche' or choix == 'centre':
					tourner(-Vg, Vd)
                else:
            		tourner(Vg, -Vd)