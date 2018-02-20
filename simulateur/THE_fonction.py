
def SuivreLigne (capteurG, capteurC, capteurD, constante, VitesseD, VitesseG):
    pass

def SuivreLigneDroite(capteurD, capteurC, capteurG, K, Vd, Vg):
    while capteurC == 1:
        while True:
            if capteurD == 1 and capteurG == 0:
                T = time.clock()
                while capteurD == 1:
                    t = time.clock()
                    tourner(Vg, Vd - K(t - T))
                    capteurD = input(capteurD)

            elif capteurG == 1 and capteurG == 0:
                T = time.clock()
                while capteurG == 1:
                    t = time.clock()
                    tourner(Vg - K(t - T), Vd)
                    capteurG = input(capteurG)

            elif capteurD == 0 and capteurG == 0:
                tourner(Vg, Vd)
                capteurG = input(capteurG)
                capteurD = input(capteurD)

            else:
                break
