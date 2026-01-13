import csv
import tri
import os
import sys
sys.setrecursionlimit(200000)

class Gestion_CSV() :
    def __init__(self):
        pass
    def chemin(self,nom : str) -> str:
        return 'CSV/'+nom+'.csv'

    def creer_csv(self,nom : str) : 
        colonne = ["nom","taille","temps","comparaison","echange"]
        with open(self.chemin(nom), 'w') as fichier:
            scribe = csv.writer(fichier,delimiter=";",lineterminator='\n')
            scribe.writerow(colonne)
            fichier.close()

        
    def ajouter_donnee_csv(self,tableau : list[list[tri.TriResultat]] ) :
        for tab in tableau :
            if ( not os.path.exists(self.chemin(tab[0].nom))) :
                self.creer_csv(tab[0].nom)
            fichier = open(self.chemin(tab[0].nom),'a')
            scribe = csv.writer(fichier,delimiter=";",lineterminator='\n')
            for resultat in tab :
               scribe.writerow([resultat.nom,resultat.taille,resultat.temps,resultat.comparaisons,resultat.echanges])
            fichier.close()
        return 0
    
    def trier_csv(self,nom : str) :
        with open(self.chemin(nom),'r') as fichier :
            lecteur = csv.reader(fichier,delimiter=';')
            donnees = list(lecteur)
            fichier.close()
        nom_colonne = donnees[0]
        self.tri_rapide(donnees[1:])
        with open(self.chemin(nom),'w') as fichier :
            scribe = csv.writer(fichier,delimiter=';',lineterminator='\n')
            scribe.writerow(nom_colonne)
            for tab in donnees[1:] :
                scribe.writerow(tab)
            fichier.close()

    def recuperer_donnee_csv(self,nom : str,min : int,max : int ,intervalle : int ) ->list[tri.TriResultat] :
        self.trier_csv(nom)
        tableau_moyenne : list[tri.TriResultat] = []
        with open(self.chemin(nom),'r') as fichier :
            lecteur = csv.reader(fichier,delimiter=';')
            donnees = list(lecteur)
            taille_cible = min
            compteur = 0 
            resultat_temporaire = tri.TriResultat("temp",0,0,0,0)
            i = 1
            while i < len(donnees) and taille_cible <= max :
                if float(donnees[i][1]) == taille_cible :
                    resultat_temporaire.nom = donnees[i][0]
                    resultat_temporaire.taille = float(donnees[i][1])
                    while ( i < len(donnees) and float(donnees[i][1]) == taille_cible):
                        resultat_temporaire.temps += float(donnees[i][2])
                        resultat_temporaire.comparaisons += float(donnees[i][3])
                        resultat_temporaire.echanges += float(donnees[i][4])
                        i += 1
                        compteur += 1

                    resultat_temporaire.temps /= compteur
                    resultat_temporaire.comparaisons /= compteur
                    resultat_temporaire.echanges /= compteur
                    tableau_moyenne.append(resultat_temporaire)
                    taille_cible += intervalle
                    resultat_temporaire = tri.TriResultat("temp",0,0,0,0)
                    compteur = 0 
                i += 1
                while i < len(donnees) and float(donnees[i][1]) > taille_cible :
                    taille_cible += intervalle
            fichier.close()
            return tableau_moyenne

    def tri_rapide(self, tab) :
        self._tri_rapide(tab, 0, len(tab) - 1)

    def _tri_rapide(self, tab, low, high):
        if low < high:
            p = self._partition(tab, low, high)
            self._tri_rapide(tab, low, p - 1)
            self._tri_rapide(tab, p + 1, high)

    def _partition(self, tab, low, high):
        pivot = tab[high]
        i = low
        for j in range(low, high):
            if float(tab[j][1]) <= float(pivot[1]) :
                tab[i], tab[j] = tab[j], tab[i]
                i += 1
        tab[i], tab[high] = tab[high], tab[i]
        return i


if __name__ == '__main__' :
    g = Gestion_CSV()