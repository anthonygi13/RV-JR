import time

# Va falloir se mettre d accord sur la structure generale de notre code
# je pensais que l utilisation de cette fonction serais un truc du style while (y a pas d'intersection): suivrelignedroite(input(capteurD), input(capteurC), input(capteurG), K, Vd, Vg)
# mais la c pas compatible
# quand un variable vaut 1 ou 0 mettez plutot des booleens
# utilisez des noms de variables clairs, c pas evident t et T...

def tourner(Vg, Vd):
    pass


def SuivreLigneDroite(capteurD, capteurC, capteurG, K, Vd, Vg):
    while capteurC == 1:
        while True:
            if capteurD == 1 and capteurG == 0:
                T = time.clock()
                while capteurD == 1:
                    t = time.clock()
                    tourner(Vg, Vd - K(t - T)) / (Vg, -Vd) #probleme la
                    capteurD = input(capteurD)

            elif capteurG == 1 and capteurG == 0:
                T = time.clock()
                while capteurG == 1:
                    t = time.clock()
                    tourner(Vg - K(t - T), Vd) / (Vg, -Vd) #probleme la
                    capteurG = input(capteurG)

            elif capteurD == 0 and capteurG == 0:
                tourner(Vg, Vd)
                capteurG = input(capteurG)
                capteurD = input(capteurD)

            else:
                break
