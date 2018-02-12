import time


def tourner(Vg, Vd):
    pass


def SuivreLigneDroite(capteurD, capteurC, capteurG, K, Vd, Vg):
    while capteurC == 1:
        while True:
            if capteurD == 1 and CapteurG == 0:
                T = time.clock()
                while CapteurD == 1:
                    t = time.clock()
                    tourner(Vg, Vd - K(t - T)) / (Vg, -Vd)
                    CapteurD = input(CapteurD)

            elif capteurG == 1 and CapteurG == 0:
                T = time.clock()
                while CapteurG == 1:
                    t = time.clock()
                    tourner(Vg - K(t - T), Vd) / (Vg, -Vd)
                    CapteurG = input(CapteurG)

            elif capteurD == 0 and capteurG == 0:
                tourner(Vg, Vd)
                CapteurG = input(CapteurG)
                CapteurD = input(CapteurD)

            else:
                break
