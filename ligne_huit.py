from ligne_courbe.py import *

def SuivreLigneHuit(capteurG, capteurC, capteurD, K, Vg, Vd, choix):
	while True:
		SuivreLigneDroite(capteurD, capteurC, capteurG, K, Vd, Vg) # la il va pas s'arreter de lire cette ligne... while True
     	k = 0 # y a pas moyen de faire en sorte que k soit un booleen et ait un nom un peu plus utile comme ça on sait a quoi il va servir ?
        while k != 1 or capteurC != 1:
       	    if choix == 'gauche' :
            	tourner(-Vg, Vd)
            elif choix == 'droite' :
            	tourner(Vg, -Vd) # pareil
            else :
            	tourner(Vg, Vd) # pareil
                
           capteurC == input(capteurC)
           
           if capteurC == 0:
                	k = 1
