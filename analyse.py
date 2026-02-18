import tkinter
import tri
import random
import gestion_csv
import math
import multiprocessing
from constante import * 


class Courbe :
     def __init__(self):
          self.t = tri.Tri()
          self.gcsv = gestion_csv.Gestion_CSV()
          self.tab : list[list[tri.TriResultat]] = []
          self.largeur = LARGEUR_FENETRE
          self.hauteur = HAUTEUR_FENETRE


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
          self.tracer_courbe()


     def lancer_tri_parrallele(self,choix : int, donnee : multiprocessing.Queue, tableau_tri : list[list[int]]) : 
          """Création d"instance unique pour chaque tri"""
          trie_process = tri.Tri()
          resultat :list[tri.TriResultat] = []
          for tab in tableau_tri :
               resultat.append(trie_process.executer(choix,tab))
               self.nb_tri_effectue.put(1)
          donnee.put(resultat)
     

     def lancer_tri_fichier(self,tableau_choix : list[int],mini : int ,maxi : int ,intervalle : int) : 
          """Récupère les données stocker en CSV, et les mets au bon format dans self.tab"""
          for choix in tableau_choix :
               self.tab.append(self.gcsv.recuperer_donnee_csv(self.t.algorithmes[choix][0],mini,maxi,intervalle))
          self.tracer_courbe()
          return 0
     
     def interface(self):
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

     def tracer_courbe(self) :
          def afficher_temps() :
               canvases[0].pack()
               canvases[1].pack_forget()
               canvases[2].pack_forget()
          def afficher_echange() :
               canvases[0].pack_forget()
               canvases[1].pack_forget()
               canvases[2].pack()
          def afficher_comparaison() :
               canvases[0].pack_forget()
               canvases[1].pack()
               canvases[2].pack_forget()

          """Fonction en charge du tracer du graphe"""
          fenetre_graphe = tkinter.Tk()
          fenetre_graphe.minsize(self.largeur,self.hauteur)
          fenetre_graphe.maxsize(self.largeur,self.hauteur)
          self.calcul()

          # Définition des métriques pour les trois graphes
          metrics : list[dict] = [
               {"key": "temps", "title": "Temps (s)", "value_attr": "temps", "par_pixel": "temps_par_pixel", "decimals": 3, "unit": "s"},
               {"key": "comparaison", "title": "Nombre comparaison", "value_attr": "comparaisons", "par_pixel": "comparaison_par_pixel", "decimals": 0, "unit": ""},
               {"key": "echange", "title": "Nombre echange", "value_attr": "echanges", "par_pixel": "echange_par_pixel", "decimals": 0, "unit": ""},
          ]

          # Création des canevas
          canvases : list[tkinter.Canvas]= []
          for m in metrics:
               c = tkinter.Canvas(fenetre_graphe, width=self.largeur, height=self.hauteur, bg=COULEUR_FOND_GRAPHE)
               c.create_text(MARGE_GAUCHE, MARGE_HAUTE-20, text=m["title"], fill=COULEUR_TEXTE_REPERE)
               c.create_text(MARGE_DROITE+50, MARGE_BASSE, text="Taille du tableau", fill=COULEUR_TEXTE_REPERE)
               c.create_line(MARGE_GAUCHE, MARGE_HAUTE, MARGE_GAUCHE, MARGE_BASSE, width=2, fill=COULEUR_AXES)
               c.create_line(MARGE_GAUCHE, MARGE_BASSE, MARGE_DROITE, MARGE_BASSE, width=2, fill=COULEUR_AXES)
               canvases.append(c)

          # Repère verticaux (temps/echange/comparaison)
          for i in range(MARGE_HAUTE, MARGE_BASSE+ESPACEMENT_VERTICAL, ESPACEMENT_VERTICAL):
               for num_graphe, parametre in enumerate(metrics):
                    val = round((i-MARGE_HAUTE) * getattr(self, parametre["par_pixel"]), parametre["decimals"]) 
                    text = str(val) + m["unit"]
                    canvases[num_graphe].create_line(MARGE_GAUCHE-10, i, MARGE_GAUCHE+10, i, width=2, fill=COULEUR_AXES)
                    canvases[num_graphe].create_line(MARGE_GAUCHE, i, MARGE_DROITE, i, width=1, fill=COULEUR_GRILLE)
                    canvases[num_graphe].create_text(MARGE_GAUCHE-30, MARGE_BASSE-i+MARGE_HAUTE, text=text, fill=COULEUR_AXES)
          # Repère horizontale : la taille
          for i in range(MARGE_GAUCHE, MARGE_DROITE+ESPACEMENT_HORIZONTAL, ESPACEMENT_HORIZONTAL):
               for canvas in canvases:
                    canvas.create_line(i, MARGE_BASSE-10, i, MARGE_BASSE+10, width=2)
                    canvas.create_line(i, MARGE_HAUTE, i, MARGE_BASSE, width=1, fill=COULEUR_GRILLE)
                    canvas.create_text(i, MARGE_BASSE+20, text=str(int(self.taille_min_tableau + self.taille_par_pixel*(i-MARGE_GAUCHE))))


          for alg_index in range(len(self.tab)):
               # légendes pour chaque canevas
               for canvas in canvases:
                    canvas.create_text(MARGE_DROITE+ESPACEMENT_HORIZONTALE_LEGENDE, ESPACEMENT_VERTICAL_LEGENDE*alg_index+MARGE_HAUTE, text=self.tab[alg_index][0].nom + " : ")
                    canvas.create_line(MARGE_DROITE+ESPACEMENT_HORIZONTALE_LEGENDE+50, ESPACEMENT_VERTICAL_LEGENDE*alg_index+MARGE_HAUTE, MARGE_DROITE+ESPACEMENT_HORIZONTALE_LEGENDE+80, ESPACEMENT_VERTICAL_LEGENDE*alg_index+MARGE_HAUTE, width=2, fill=self.tab[alg_index][0].couleur)

               # tracer des courbes pour cet algorithme sur tous les canevas
               precedents = [(MARGE_GAUCHE, MARGE_BASSE) for _ in metrics]
               for resultat in self.tab[alg_index]:
                    x = MARGE_GAUCHE + (resultat.taille - self.taille_min_tableau) / self.taille_par_pixel
                    for graphe, parametre in enumerate(metrics):
                         y = MARGE_BASSE - getattr(resultat, parametre["value_attr"]) / getattr(self, parametre["par_pixel"]) 
                         canvases[graphe].create_line(precedents[graphe][0], precedents[graphe][1], x, y, fill=self.tab[alg_index][0].couleur)
                         precedents[graphe] = (x, y)


          # Tracer des courbes théoriques (repères) en une seule passe
          precs = [[(MARGE_GAUCHE, MARGE_BASSE) for _ in range(3)]for _  in range(len(metrics))]

          for i in range(int(self.tab[0][0].taille), int(self.tab[0][-1].taille),int(self.tab[0][1].taille-self.tab[0][0].taille)):
               x = MARGE_GAUCHE + (i - self.taille_min_tableau) / self.taille_par_pixel

               y = MARGE_BASSE -(i * TEMPS_THEORIQUE_OPERATION) /self.temps_par_pixel
               if y > MARGE_GAUCHE : 
                    canvases[0].create_line(precs[0][0][0],precs[0][0][1],x,y)
                    precs[0][0] = (x,y)
               y = MARGE_BASSE - (i * math.log(i) * TEMPS_THEORIQUE_OPERATION ) /self.temps_par_pixel
               if y > MARGE_HAUTE :
                    canvases[0].create_line(precs[0][1][0],precs[0][1][1],x,y)
                    precs[0][1] = (x,y)
               y = MARGE_BASSE -(i * i * TEMPS_THEORIQUE_OPERATION) /self.temps_par_pixel
               if y > MARGE_HAUTE : 
                    canvases[0].create_line(precs[0][2][0],precs[0][2][1],x,y)
                    precs[0][2] = (x,y)
               for j in range(1,len(metrics)) :
                    y = MARGE_BASSE - (i) / getattr(self, metrics[j]["par_pixel"])
                    if y > MARGE_HAUTE : 
                         canvases[j].create_line(precs[j][0][0], precs[j][0][1], x, y)
                         precs[j][0] = (x, y)
                    y = MARGE_BASSE - (i*math.log(i)) / getattr(self, metrics[j]["par_pixel"])
                    if y > MARGE_HAUTE : 
                         canvases[j].create_line(precs[j][1][0], precs[j][1][1], x, y)
                         precs[j][1] = (x, y)
                    y = MARGE_BASSE - (i*i) / getattr(self, metrics[j]["par_pixel"])
                    if y > MARGE_HAUTE : 
                         canvases[j].create_line(precs[j][2][0], precs[j][2][1], x, y)
                         precs[j][2] = (x, y)
          


          for j in range(len(metrics)) :
               canvases[j].create_text(precs[j][0][0],precs[j][0][1]-10,text="N")
               canvases[j].create_text(precs[j][1][0],precs[j][1][1]-10,text="N*log(N)")
               canvases[j].create_text(precs[j][2][0],precs[j][2][1]-10,text="N*N")


          # Option radio pour changer d'affichage
          option = tkinter.IntVar(value=1)
          frame_options = tkinter.Frame(fenetre_graphe)
          frame_options.pack()
          tkinter.Radiobutton(frame_options, text='Temps', variable=option, value=1, command=afficher_temps).pack(side='left')
          tkinter.Radiobutton(frame_options, text='Echange', variable=option, value=2, command=afficher_echange).pack(side='left')
          tkinter.Radiobutton(frame_options, text='Comparaison', variable=option, value=3, command=afficher_comparaison).pack(side='left')
          # affichage initial
          canvases[0].pack()
          fenetre_graphe.mainloop()
          return 0

     

     
     def calcul(self) :
          """Fonction effectuant les calculs nécessaire au tracé du graphe"""
          self.temps = 0
          self.echange = 0
          self.comparaison = 0
          self.taille_min_tableau = self.tab[0][0].taille
          self.taille_max_tableau = self.tab[0][0].taille
          for tableau in self.tab :
               self.temps = max(max(tab.temps for tab in tableau),self.temps)
               self.echange = max(max(tab.echanges for tab in tableau),self.echange)
               self.comparaison = max(max(tab.comparaisons for tab in tableau),self.comparaison)
               self.taille_min_tableau = min(min(tab.taille for tab in tableau),self.taille_min_tableau)
               self.taille_max_tableau = max(max(tab.taille for tab in tableau),self.taille_max_tableau)
          self.temps_par_pixel = self.temps / (MARGE_BASSE-MARGE_HAUTE)
          self.comparaison_par_pixel = self.comparaison / (MARGE_BASSE-MARGE_HAUTE)
          self.echange_par_pixel = self.echange / (MARGE_BASSE-MARGE_HAUTE)
          self.taille_par_pixel = (self.taille_max_tableau - self.taille_min_tableau) / (MARGE_DROITE-MARGE_GAUCHE)
     
if __name__ == "__main__" :
     c = Courbe()
     c.interface()

