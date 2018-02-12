def tourner(Vg, Vd):
    pass


def SuivreLigneHuit(capteurG, capteurC, capteurD, K, Vg, Vd, choix):
    while True:
        SuivreLigneDroite(capteurD, capteurC, capteurG, K, Vd, Vg)
        k = 0
        while k != 1 or capteurC != 1:
            if choix == 'gauche' :
                tourner(-Vg, Vd)
            elif choix == 'droite' :
                tourner(Vg, -Vd)
            else :
                tourner(Vg, Vd)
            capteurC == input(capteurC)

            if capteurC == 0:
                k = 1
