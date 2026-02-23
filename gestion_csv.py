import csv
import os
from constante import *
from tri import TriResultat

class Gestion_CSV() :
    def __init__(self):
        pass
    def chemin(self,nom : str) -> str:
        """Prend le nom des fichiers CSV et renvoie le chemin"""
        return DOSSIER_CSV+"/"+nom+'.csv'

    def creer_csv(self,nom : str) : 
        """Prend le nom d'un fichier et créer automatiquement le fichier et l'entête"""
        with open(self.chemin(nom), 'w') as fichier:
            scribe = csv.writer(fichier,delimiter=SEPARATEUR_CSV,lineterminator='\n')
            scribe.writerow(["nom", "taille", "temps", "comparaison", "echange","couleur"])
            fichier.close()

        
    def ajouter_donnee_csv(self,tableau : list[list[TriResultat]] ) :
        """Prend la liste des tris effectué et ajoute dans les fichiers correspondant les réultats"""
        for tab in tableau :
            if ( not os.path.exists(self.chemin(tab[0].nom))) :
                self.creer_csv(tab[0].nom)
            fichier = open(self.chemin(tab[0].nom),'a')
            scribe = csv.writer(fichier,delimiter=SEPARATEUR_CSV,lineterminator='\n')
            for resultat in tab :
               scribe.writerow([resultat.nom,resultat.taille,resultat.temps,resultat.comparaisons,resultat.echanges,resultat.couleur])
            fichier.close()
        return 0
    
    def trier_csv(self,nom : str) :
        """Prend le nom d'un fichier et le trie par ordre croissant de la taille"""
        with open(self.chemin(nom),'r') as fichier :
            lecteur = csv.reader(fichier,delimiter=SEPARATEUR_CSV)
            donnees = list(lecteur)
            fichier.close()
        nom_colonne = donnees[0]
        donnees = sorted(donnees[1:], key=lambda donnee: int(donnee[1]))
        with open(self.chemin(nom),'w') as fichier :
            scribe = csv.writer(fichier,delimiter=SEPARATEUR_CSV,lineterminator='\n')
            scribe.writerow(nom_colonne)
            for tab in donnees :
                scribe.writerow(tab)
            fichier.close() 

    def recuperer_donnee_csv(self,nom : str,min : int,max : int ,intervalle : int ) ->list[TriResultat] :
        """Récupère les données du fichier dans et les renvoie au format utilisable"""
        self.trier_csv(nom)
        tableau_moyenne : list[TriResultat] = []

        # Ouverture du fichier
        with open(self.chemin(nom),'r') as fichier :
            lecteur = csv.reader(fichier,delimiter=SEPARATEUR_CSV)
            donnees = list(lecteur)
            taille_cible = min
            compteur = 0 
            resultat_temporaire = TriResultat("temp",0,0,0,0,"red")
            i = 1

            # Convertion du format tableau au format TriResultat
            try :
                while i < len(donnees) and taille_cible <= max :
                    if float(donnees[i][1]) == taille_cible :
                        resultat_temporaire.nom = donnees[i][0]
                        resultat_temporaire.couleur = donnees[i][-1]
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
                        resultat_temporaire = TriResultat("temp",0,0,0,0,"red")
                        compteur = 0 
                    i += 1
                    while i < len(donnees) and float(donnees[i][1]) > taille_cible :
                        taille_cible += intervalle
                fichier.close()
                return tableau_moyenne
            except ValueError:
                print("Une valeur incohérente est enregistré")


if __name__ == '__main__' :
    g = Gestion_CSV()