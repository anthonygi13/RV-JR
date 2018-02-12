import time

# Va falloir se mettre d accord sur la structure generale de notre code
# je pensais que l utilisation de cette fonction serais un truc du style while (y a pas d'intersection): suivrelignedroite(input(capteurD), input(capteurC), input(capteurG), K, Vd, Vg)
# mais la c pas compatible
# quand un variable vaut 1 ou 0 mettez plutot des booleens

def SuivreLigneDroite(capteurD, capteurC, capteurG, K, Vd, Vg):
	while capteurC == 1:
	#capteurC c est un argument de la fonction il va pas changer au cours de l'execution de cette fonction...
		While True :
		If capteurD == 1 and CapteurG == 0:
			T = time.clock()
			While CapteurD == 1 :
				t = time.clock()
				Tourner (Vg, Vd - K(t - T)) /(Vg, -Vd)
				CapteurD = input(CapteurD)
                
		Elif capteurG == 1 and CapteurG == 0:
			T = time.clock()
			While CapteurG == 1:
				t = time.clock()
				Tourner (Vg - K(t - T), Vd) /(Vg, -Vd)
				CapteurG = input(CapteurG)
                
		Elif capteurD == 0 and capteurG == 0:
			Tourner (Vg,Vd)
			CapteurG = input(CapteurG)
			CapteurD = input(CapteurD)
            
		Else :
			Break
