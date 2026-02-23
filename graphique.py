import tkinter
from tri import TriResultat
import math
from constante import * 


class Courbe :
     def __init__(self, tableau : list[list[TriResultat]]):
          self.largeur = LARGEUR_FENETRE
          self.hauteur = HAUTEUR_FENETRE
          self.tab : list[list[TriResultat]] = tableau
          self.metrics : list[dict] = [
               {"key": "temps", "title": "Temps (s)", "value_attr": "temps", "par_pixel": "temps_par_pixel", "decimals": 3, "unit": "s"},
               {"key": "comparaison", "title": "Nombre comparaison", "value_attr": "comparaisons", "par_pixel": "comparaison_par_pixel", "decimals": 0, "unit": ""},
               {"key": "echange", "title": "Nombre echange", "value_attr": "echanges", "par_pixel": "echange_par_pixel", "decimals": 0, "unit": ""},
          ]
          self.canvas = []
          self.tableau_ligne = []
          self.tableau_ligne_affiche = []
          self.tableau_ligne_surligne = []
          self.main_boucle()


     def tracer_canvas(self,fenetre) :
          for m in self.metrics:
               c = tkinter.Canvas(fenetre, width=MARGE_DROITE+30, height=self.hauteur, bg=COULEUR_FOND_GRAPHE)
               c.create_text(MARGE_GAUCHE, MARGE_HAUTE-20, text=m["title"], fill=COULEUR_TEXTE_REPERE)
               c.create_text(MARGE_DROITE+50, MARGE_BASSE, text="Taille du tableau", fill=COULEUR_TEXTE_REPERE)
               c.create_line(MARGE_GAUCHE, MARGE_HAUTE, MARGE_GAUCHE, MARGE_BASSE, width=2, fill=COULEUR_AXES)
               c.create_line(MARGE_GAUCHE, MARGE_BASSE, MARGE_DROITE, MARGE_BASSE, width=2, fill=COULEUR_AXES)
               self.canvas.append(c)

     def tracer_repere(self) :
          # Repère verticaux (temps/echange/comparaison)
          for i in range(MARGE_HAUTE, MARGE_BASSE+ESPACEMENT_VERTICAL, ESPACEMENT_VERTICAL):
               for num_graphe, parametre in enumerate(self.metrics):
                    val = round((i-MARGE_HAUTE) * getattr(self, parametre["par_pixel"]), parametre["decimals"]) 
                    text = str(val) + parametre["unit"]
                    self.canvas[num_graphe].create_line(MARGE_GAUCHE-10, i, MARGE_GAUCHE+10, i, width=2, fill=COULEUR_AXES)
                    self.canvas[num_graphe].create_line(MARGE_GAUCHE, i, MARGE_DROITE, i, width=1, fill=COULEUR_GRILLE)
                    self.canvas[num_graphe].create_text(MARGE_GAUCHE-30, MARGE_BASSE-i+MARGE_HAUTE, text=text, fill=COULEUR_AXES)
          # Repère horizontale : la taille
          for i in range(MARGE_GAUCHE, MARGE_DROITE+ESPACEMENT_HORIZONTAL, ESPACEMENT_HORIZONTAL):
               for canvas in self.canvas:
                    canvas.create_line(i, MARGE_BASSE-10, i, MARGE_BASSE+10, width=2)
                    canvas.create_line(i, MARGE_HAUTE, i, MARGE_BASSE, width=1, fill=COULEUR_GRILLE)
                    canvas.create_text(i, MARGE_BASSE+20, text=str(int(self.taille_min_tableau + self.taille_par_pixel*(i-MARGE_GAUCHE))))

     def tracer_courbe(self) :
          self.tableau_ligne = [ [ [] for _ in range(len(self.canvas)) ]for _ in range(len(self.tab)) ]
          for alg_index in range(len(self.tab)):
               precedents = [(MARGE_GAUCHE, MARGE_BASSE) for _ in self.metrics]
               i = 0
               while i < len(self.tab[alg_index]) -self.nombre_parcourir :
                    x = MARGE_GAUCHE + (self.tab[alg_index][i].taille - self.taille_min_tableau) / self.taille_par_pixel
                    for graphe, parametre in enumerate(self.metrics):
                         y = 0 
                         for j in range(i,i+self.nombre_parcourir) :
                              y += MARGE_BASSE - getattr(self.tab[alg_index][j], parametre["value_attr"]) / getattr(self, parametre["par_pixel"]) 
                         y /= self.nombre_parcourir
                         ligne = self.canvas[graphe].create_line(precedents[graphe][0], precedents[graphe][1], x, int(y), fill=self.tab[alg_index][0].couleur,width=1)
                         self.tableau_ligne[alg_index][graphe].append(ligne)
                         precedents[graphe] = (x, int(y))
                    i += self.nombre_parcourir
     
     def tracer_courbe_repere(self) : 
     # Tracer des courbes théoriques (repères) en une seule passe
          precs = [[(MARGE_GAUCHE, MARGE_BASSE) for _ in range(3)]for _  in range(len(self.metrics))]

          for i in range(int(self.tab[0][0].taille), int(self.tab[0][-1].taille),int(self.tab[0][1].taille-self.tab[0][0].taille)):
               x = MARGE_GAUCHE + (i - self.taille_min_tableau) / self.taille_par_pixel

               y = MARGE_BASSE -(i * TEMPS_THEORIQUE_OPERATION) /self.temps_par_pixel
               if y > MARGE_GAUCHE : 
                    self.canvas[0].create_line(precs[0][0][0],precs[0][0][1],x,y)
                    precs[0][0] = (x,y)
               y = MARGE_BASSE - (i * math.log(i) * TEMPS_THEORIQUE_OPERATION ) /self.temps_par_pixel
               if y > MARGE_HAUTE :
                    self.canvas[0].create_line(precs[0][1][0],precs[0][1][1],x,y)
                    precs[0][1] = (x,y)
               y = MARGE_BASSE -(i * i * TEMPS_THEORIQUE_OPERATION) /self.temps_par_pixel
               if y > MARGE_HAUTE : 
                    self.canvas[0].create_line(precs[0][2][0],precs[0][2][1],x,y)
                    precs[0][2] = (x,y)
               for j in range(1,len(self.metrics)) :
                    y = MARGE_BASSE - (i) / getattr(self, self.metrics[j]["par_pixel"])
                    if y > MARGE_HAUTE : 
                         self.canvas[j].create_line(precs[j][0][0], precs[j][0][1], x, y)
                         precs[j][0] = (x, y)
                    y = MARGE_BASSE - (i*math.log(i)) / getattr(self, self.metrics[j]["par_pixel"])
                    if y > MARGE_HAUTE : 
                         self.canvas[j].create_line(precs[j][1][0], precs[j][1][1], x, y)
                         precs[j][1] = (x, y)
                    y = MARGE_BASSE - (i*i) / getattr(self, self.metrics[j]["par_pixel"])
                    if y > MARGE_HAUTE : 
                         self.canvas[j].create_line(precs[j][2][0], precs[j][2][1], x, y)
                         precs[j][2] = (x, y)


          for j in range(len(self.metrics)) :
               self.canvas[j].create_text(precs[j][0][0],precs[j][0][1]-10,text="N")
               self.canvas[j].create_text(precs[j][1][0],precs[j][1][1]-10,text="N*log(N)")
               self.canvas[j].create_text(precs[j][2][0],precs[j][2][1]-10,text="N*N")


     def ecrire_legende(self,fenetre) :
          tableau_affichage = []
          tableau_epaisseur = []
          for algo in range(len(self.tab)) : 
               visibilite = tkinter.IntVar(value=1)
               epaisseur = tkinter.IntVar(value=1)
               tableau_affichage.append(visibilite)
               tableau_epaisseur.append(epaisseur)
               tkinter.Checkbutton(fenetre,text=self.tab[algo][0].nom + " : ―― ",fg=self.tab[algo][0].couleur,variable=visibilite, command=lambda: self.changer_visibilite_ligne(tableau_affichage)).pack(anchor="w")
               tkinter.Checkbutton(fenetre,variable=epaisseur, command=lambda: self.changer_epaisseur(tableau_epaisseur)).pack(anchor="nw")

     def bouton_changer_affichage(self,fenetre) :
          option = tkinter.IntVar(value=0)
          tkinter.Radiobutton(fenetre, text='Temps', variable=option, value=0, command=lambda: self.changer_affichage(option.get())).pack(side='left')
          tkinter.Radiobutton(fenetre, text='Comparaison', variable=option, value=1, command=lambda: self.changer_affichage(option.get())).pack(side='left')
          tkinter.Radiobutton(fenetre, text='Echange', variable=option, value=2, command=lambda: self.changer_affichage(option.get())).pack(side='left')

     def changer_visibilite_ligne(self,tableau_affichage) :
          tableau_choix = [i for i, var in enumerate(tableau_affichage) if var.get() == 1]
          max = len(self.tab)
          for i in range(max) :
               if i in tableau_choix :
                    if self.tableau_ligne_affiche[i] == True : 
                         continue
                    self.tableau_ligne_affiche[i] = True
                    for canva in range (len(self.tableau_ligne[i])):
                         for ligne in self.tableau_ligne[i][canva] : 
                              self.canvas[canva].itemconfig(ligne, state="normal")
               else :
                    if self.tableau_ligne_affiche[i] == False : 
                         continue
                    self.tableau_ligne_affiche[i] = False
                    for canva in range (len(self.tableau_ligne[i])):
                         for ligne in self.tableau_ligne[i][canva] : 
                              self.canvas[canva].itemconfig(ligne, state="hidden")
     

     def changer_epaisseur(self,tableau_epaisseur) : 
          tableau_choix = [i for i, var in enumerate(tableau_epaisseur) if var.get() == 1]
          max = len(self.tab)
          for i in range(max) :
               if i in tableau_choix :
                    if self.tableau_ligne_surligne[i] == True : 
                         continue
                    self.tableau_ligne_surligne[i] = True
                    for canva in range (len(self.tableau_ligne[i])):
                         for ligne in self.tableau_ligne[i][canva] : 
                              self.canvas[canva].itemconfig(ligne, width=4)
               else :
                    if self.tableau_ligne_surligne[i] == False : 
                         continue
                    self.tableau_ligne_surligne[i] = False
                    for canva in range (len(self.tableau_ligne[i])):
                         for ligne in self.tableau_ligne[i][canva] : 
                              self.canvas[canva].itemconfig(ligne, width=1)

     def changer_affichage(self,choix : int) :
          for i in range(len(self.canvas)) :
               if i == choix :
                    self.canvas[i].pack(side="left")
               else :
                    self.canvas[i].pack_forget()  

     def main_boucle(self) :
          # Initialisation du graphe
          fenetre_graphe = tkinter.Tk()
          fenetre_graphe.title("Graphiques")
          fenetre_graphe.minsize(self.largeur,self.hauteur)
          fenetre_graphe.maxsize(self.largeur,self.hauteur)
          self.calcul_permanent()
          self.calcul_temp()
          frame_graphe_legend = tkinter.Frame(fenetre_graphe,width=self.largeur,height=self.hauteur)
          frame_legend = tkinter.Frame(frame_graphe_legend,width=self.largeur - MARGE_DROITE, height=int(self.hauteur/2))
          frame_option = tkinter.Frame(fenetre_graphe)
          self.tracer_canvas(frame_graphe_legend)
          self.tracer_repere()
          self.tracer_courbe()
          self.tracer_courbe_repere()
          self.ecrire_legende(frame_legend)
          self.bouton_changer_affichage(frame_option)

          # affichage initial
          self.tableau_ligne_affiche = [True for _ in range(len(self.tab))]
          self.tableau_ligne_surligne = [True for _ in range(len(self.tab))]


          self.changer_affichage(0)
          frame_option.pack(anchor="n")
          frame_graphe_legend.pack(anchor="w")
          frame_legend.pack(side="right",anchor="n")
          fenetre_graphe.mainloop()
     

     

     
     def calcul_permanent(self) :
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

     def calcul_temp(self) :
          if ( (MARGE_DROITE - MARGE_GAUCHE) / len(self.tab[0]) < NOMBRE_PIXEL_ECART_MINIMUM  ) :
               self.nombre_parcourir = int(NOMBRE_PIXEL_ECART_MINIMUM / ((MARGE_DROITE-MARGE_GAUCHE) / len(self.tab[0]) ))
          else :
               self.nombre_parcourir = 1
     