import time


def tourner(vg, vd):
    pass


def SuivreLigneDroite(capteurD, capteurG, K, Vg, Vd):
    while True:
        if capteurD == 1 and capteurG == 0:
            T = time.clock()
            while capteurD == 1:
                t = time.clock()
                tourner(Vg, Vd - K(t - T)) / (Vg, -Vd)
                capteurD = input(capteurD)

        elif capteurG == 1 and capteurG == 0:
            T = time.clock()
            while capteurG == 1:
                t = time.clock()
                tourner(Vg - K(t - T), Vd) / (Vg, -Vd)
                capteurG = input(capteurG)

        elif capteurD == 0 and capteurG == 0:
            tourner(Vg, Vd)
            capteurG = input(capteurG)
            capteurD = input(capteurD)
        else:
            break


