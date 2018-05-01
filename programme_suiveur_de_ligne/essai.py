
def traitement_chemin(chemin, choix):

    if choix == 'droite':
        for i in range (len(chemin)):
            if chemin[i] == 'demi-tour':
                if chemin[i+1] == 'droite' :
                    chemin[i+1] = 'face'
                elif chemin[i+1] == 'face':
                    chemin[i+1] = 'gauche'
                else:
                    chemin[i+1] = 'demi-tour'
                del chemin[i]
                del chemin[i-1]

    if choix == 'gauche':
        for i in range (len(chemin)):
            if chemin[i] == 'demi-tour':
                if chemin[i+1] == 'gauche' :
                    chemin[i+1] = 'face'
                elif chemin[i+1] == 'face':
                    chemin[i+1] = 'droite'
                else:
                    chemin[i+1] = 'demi-tour'
                del chemin[i]
                del chemin[i-1]

    return chemin

