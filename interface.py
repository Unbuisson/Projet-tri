import tkinter
import multiprocessing
import random
from constante import *
from tri import * 
from gestion_csv import Gestion_CSV
from graphique import Courbe

class Interface : 
    def __init__(self):
        self.t = Tri()
        self.gcsv = Gestion_CSV()
        self.tab : list[list[TriResultat]] = []

    def generer_tableau(self,nombre_element : int) -> list[int]: 
        """Génère un tableau de taille n d'entier compris entre 0 2 puissance 14"""
        return [random.randint(0, VALEUR_MAX_TABLEAU) for _ in range (nombre_element)]


    def lancer_tri(self, tableau_choix: list[int], mini: int, maxi: int, intervalle: int): 
        """Fonction en charge de lancer les tris en parrallele"""
        tableau_process : list[multiprocessing.Process] = []
        tableau_a_trier : list[list[int]] = []
        fenetre_chargement = tkinter.Tk()
        fenetre_chargement.minsize(width=LARGEUR_CHARGEMENT,height=HAUTEUR_CHARGEMENT)
        fenetre_chargement.maxsize(width=LARGEUR_CHARGEMENT,height=HAUTEUR_CHARGEMENT)
        canvas = tkinter.Canvas(fenetre_chargement,width=LARGEUR_CHARGEMENT,height=HAUTEUR_CHARGEMENT,background="red")
        affichage_pourcentage = canvas.create_text(LARGEUR_CHARGEMENT/2-20,HAUTEUR_CHARGEMENT/2,text="0%",fill="white",width=90)
        canvas.pack()
        donnees = multiprocessing.Queue()
        self.nb_tri_effectue = multiprocessing.Queue()
        compteur = 0
        nb_tri_a_effectue = len(range(mini, maxi + 1, intervalle)) * len(tableau_choix)
        # Génère les tableaux pour que les tris travaille sur des tableaux identiques
        for i in range(mini, maxi + 1, intervalle):
            tableau_a_trier.append(self.generer_tableau(i))

        # Création et lancement des process et parallèle
        for j in range(len(tableau_choix)):
            process = multiprocessing.Process(target=self.lancer_tri_parrallele, args=(tableau_choix[j],donnees,tableau_a_trier))
            tableau_process.append(process)
            process.start()

        while compteur < nb_tri_a_effectue :
            compteur += self.nb_tri_effectue.get()
            pourcentage = (compteur/nb_tri_a_effectue)*100
            canvas.itemconfig(affichage_pourcentage,text=str(int(pourcentage))+ "%",width=90)
            fenetre_chargement.update()
         
        fenetre_chargement.destroy()
        fenetre_chargement = None
        # Récupération des données de chaque process une fois terminée
        for _ in tableau_process:
            resultat = donnees.get() 
            self.tab.append(resultat)
        # Fin des process
        for p in tableau_process:
            p.join()

        self.gcsv.ajouter_donnee_csv(self.tab)
        Courbe(self.tab)


    def lancer_tri_parrallele(self,choix : int, donnee : multiprocessing.Queue, tableau_tri : list[list[int]]) : 
        """Création d"instance unique pour chaque tri"""
        trie_process = Tri()
        resultat :list[TriResultat] = []
        for tab in tableau_tri :
            resultat.append(trie_process.executer(choix,tab))
            self.nb_tri_effectue.put(1)
        donnee.put(resultat)
     

    def lancer_tri_fichier(self,tableau_choix : list[int],mini : int ,maxi : int ,intervalle : int) : 
        """Récupère les données stocker en CSV, et les mets au bon format dans self.tab"""
        for choix in tableau_choix :
            self.tab.append(self.gcsv.recuperer_donnee_csv(self.t.algorithmes[choix][0],mini,maxi,intervalle))
        Courbe(self.tab)
     
    def lancer(self):
        """Interface de selection des tris"""
        def recuperer_donnees():
            """Récupération et vérification des données"""
            tableau_choix = [i + 1 for i, var in enumerate(vars_tris) if var.get() == 1]
            if len(tableau_choix) == 0 :
                print("Aucun tri selectionné")
                return

            try :
                mini = int(valeur_min.get())
                maxi = int(valeur_max.get())
                intervalle = int(valeur_intervalle.get())
            except ValueError:
                print("Veuillez entrer des entiers")
                return

            if mini >= maxi or intervalle <= 0:
                print("Paramètres incohérents")
                return

            fenetre_interface.destroy()
            if fichier.get() == 1 :
                self.lancer_tri_fichier(tableau_choix,mini,maxi,intervalle)
            else :
                self.lancer_tri(tableau_choix, mini, maxi, intervalle)
            return
          
        fenetre_interface = tkinter.Tk()
        fenetre_interface.minsize(width=LARGEUR_INTERFACE, height=HAUTEUR_INTERFACE)
        fenetre_interface.maxsize(width=LARGEUR_INTERFACE, height=HAUTEUR_INTERFACE)

        vars_tris = []
        for nom in self.t.algorithmes.values():
            var = tkinter.IntVar()
            vars_tris.append(var)
            tkinter.Checkbutton(fenetre_interface,text=nom[0],variable=var).pack(anchor="w")

        tkinter.Label(fenetre_interface, text="Taille minimale").pack()
        valeur_min = tkinter.Entry(fenetre_interface)
        valeur_min.pack()

        tkinter.Label(fenetre_interface, text="Taille maximale").pack()
        valeur_max = tkinter.Entry(fenetre_interface)
        valeur_max.pack()

        tkinter.Label(fenetre_interface, text="Intervalle").pack()
        valeur_intervalle = tkinter.Entry(fenetre_interface)
        valeur_intervalle.pack()

        tkinter.Label(fenetre_interface, text="Fichier").pack()
        fichier = tkinter.IntVar()
        tkinter.Checkbutton(fenetre_interface,variable=fichier).pack()

        valider = tkinter.Button(fenetre_interface,text="Valider",command=recuperer_donnees)
        valider.pack()

        fenetre_interface.mainloop()
