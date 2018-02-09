def SuivreLigneDroite(CapteurD, CapteuG):
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
