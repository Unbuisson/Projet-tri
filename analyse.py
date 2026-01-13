import tkinter
import tri
import random
import gestion_csv
import math
import multiprocessing

class Courbe :
     def __init__(self):
          self.t = tri.Tri()
          self.gcsv = gestion_csv.Gestion_CSV()
          self.tab : list[list[tri.TriResultat]] = []
          self.largeur = 1100
          self.hauteur = 900
          self.couleur = ["red","blue","green","grey","brown","pink","purple","orange","cyan"]
          self.fenetre_chargement = None
          self.label_pourcentage = None

     def generer_tableau(self,nombre_element : int) -> list[int]:
          return [random.randint(0, pow(2,14)) for _ in range (nombre_element)]


     def lancer_tri(self, tableau_choix: list[int], mini: int, maxi: int, intervalle: int):
          tableau_process : list[multiprocessing.Process] = []
          tableau_a_trier : list[list[int]] = []
          donnees = multiprocessing.Queue()
          
          for i in range(mini, maxi + 1, intervalle):
               tableau_a_trier.append(self.generer_tableau(i))
          for j in range(len(tableau_choix)):
               process = multiprocessing.Process(target=self.lancer_tri_parrallele, args=(tableau_choix[j],donnees,tableau_a_trier))
               tableau_process.append(process)
               process.start()
          for _ in tableau_process:
               resultat = donnees.get() 
               self.tab.append(resultat)

          for p in tableau_process:
               p.join()

          self.gcsv.ajouter_donnee_csv(self.tab)
          self.tracer_courbe()


     def lancer_tri_parrallele(self,choix : int, donnee : multiprocessing.Queue, tableau_tri : list[list[int]]) :
          trie_process = tri.Tri()
          resultat :list[tri.TriResultat] = []
          for tab in tableau_tri :
               resultat.append(trie_process.executer(choix,tab))
          donnee.put(resultat)
     

     def lancer_tri_fichier(self,tableau_choix : list[int],mini : int ,maxi : int ,intervalle : int) :
          for choix in tableau_choix :
               self.tab.append(self.gcsv.recuperer_donnee_csv(self.t.algorithmes[choix][0],mini,maxi,intervalle))
          self.tracer_courbe()
          return 0
     
     def interface(self):
          fenetre_interface = tkinter.Tk()
          fenetre_interface.minsize(width=300, height=500)
          fenetre_interface.maxsize(width=300, height=500)

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
          def recuperer_donnees():
               tableau_choix = []
               for i, var in enumerate(vars_tris):
                    if var.get() == 1:
                         tableau_choix.append(i + 1)
                    

                    mini = int(valeur_min.get())
                    maxi = int(valeur_max.get())
                    intervalle = int(valeur_intervalle.get())

               if mini >= maxi or intervalle <= 0:
                    print("Paramètres incohérents")
                    return

               fenetre_interface.destroy()
               if fichier.get() == 1 :
                    self.lancer_tri_fichier(tableau_choix,mini,maxi,intervalle)
               else :
                    self.lancer_tri(tableau_choix, mini, maxi, intervalle)

          valider = tkinter.Button(fenetre_interface,text="Valider",command=recuperer_donnees)
          valider.pack()

          fenetre_interface.mainloop()



     def tracer_courbe(self) :
          #création de la fenetre
          self.calcul()
          fenetre_graphe = tkinter.Tk()
          fenetre_graphe.minsize(self.largeur,self.hauteur)
          fenetre_graphe.maxsize(self.largeur,self.hauteur)
          graphe = tkinter.Canvas(fenetre_graphe,width=self.largeur,height=self.hauteur,bg='ivory')
          graphe.create_text(110,80,text="Temps (s)",fill='red')
          graphe.create_text(60,830,text="Taille du tableau")
          graphe.create_line(110,100,110,850,width=2) #Ordonnée du temps
          graphe.create_line(110,850,990,850,width=2) #Abcisse taille du tableau
          #création des repaires
          for i in range(150,950,50) :
               graphe.create_line(100,i,120,i,width=2)
               graphe.create_line(110,i,990,i,width=1,fill="lightgrey")
               graphe.create_text(60,1000-i,text=str(round((i-150)*self.temps_par_pixel,5)))
          for i in range (110,1030,40) :
               graphe.create_line(i,840,i,860,width=2)
               graphe.create_line(i,100,i,850,width=1,fill="lightgrey")
               graphe.create_text(i,880,text=str(int(self.taille_min_tableau+self.taille_par_pixel*(i-110))))
          #tracer de la courbe 
          for i in range(len(self.tab)) :
               #légende
               graphe.create_text(150+200*i,50,text=self.tab[i][0].nom + " : ")
               graphe.create_line(200+i*200,50,220+i*200,50,width=2,fill=self.couleur[i])
               precedent = None
               #courbe
               for resultat in self.tab[i] :
                    x = 110 + (resultat.taille - self.taille_min_tableau) / self.taille_par_pixel
                    y = 850 - resultat.temps / self.temps_par_pixel
                    if precedent:
                         graphe.create_line(precedent[0], precedent[1],x, y,fill=self.couleur[i])
                    precedent = (x, y)
          
          #courbe repaire
          tab_n_carre = multiprocessing.Queue()
          tab_n_logn =  multiprocessing.Queue()
          tab_n =  multiprocessing.Queue()
          process_nCarre = multiprocessing.Process(target=self.nCarre,args=(self.temp_theorique_operation,self.temps_par_pixel,tab_n_carre,self.tab[0]))
          process_nLogn = multiprocessing.Process(target=self.nLogN,args=(self.temp_theorique_operation,self.temps_par_pixel,tab_n_logn,self.tab[0]))
          process_n = multiprocessing.Process(target=self.n,args=(self.temp_theorique_operation,self.temps_par_pixel,tab_n,self.tab[0]))
          process_nCarre.start()
          process_nLogn.start()
          process_n.start()
          tab1,tab2,tab3 =  tab_n_carre.get(),tab_n_logn.get(),tab_n.get()
          process_nCarre.join()
          process_nLogn.join()
          process_n.join()
          for i in range (0,len(self.tab[0])) :
               if i != 0 :
                    x = 110 + (self.tab[0][i].taille - self.taille_min_tableau) / self.taille_par_pixel
                    if (tab1[i] > 150) :
                         graphe.create_line(x_prec,tab1[i-1],x,tab1[i])
                         derniere_coordonne = (x,tab1[i])
                    graphe.create_line(x_prec,tab2[i-1],x,tab2[i])
                    graphe.create_line(x_prec,tab3[i-1],x,tab3[i])
               x_prec = x 

          graphe.create_text(x,tab3[-1]-15,text="N")
          graphe.create_text(derniere_coordonne[0],derniere_coordonne[1]-15,text="N*N")
          graphe.create_text(x,tab2[-1]-15,text="N*log(N)")

          graphe.pack()
          fenetre_graphe.mainloop()
          return 0
     
     def nCarre (self,temp_theorique_operation,temps_par_pixel,tab_n_carre,tab_ex) : 
          tab = []
          for resultat in tab_ex :
               tab.append(850 - (resultat.taille * resultat.taille * temp_theorique_operation)  / temps_par_pixel)
          tab_n_carre.put(tab)
     def nLogN(self,temp_theorique_operation,temps_par_pixel,tab_n_logn,tab_ex) :
          tab = []
          for resultat in tab_ex :
              tab.append(850 - (resultat.taille * math.log(resultat.taille) * temp_theorique_operation)  / temps_par_pixel)
          tab_n_logn.put(tab)
     def n(self,temp_theorique_operation,temps_par_pixel,tab_n,tab_ex) :
          tab = []
          for resultat in tab_ex :
                    tab.append(850 - (resultat.taille * temp_theorique_operation)  / temps_par_pixel)
          tab_n.put(tab)
     
     def calcul(self) :
          self.temps = 0
          self.taille_min_tableau = self.tab[0][0].taille
          self.taille_max_tableau = self.tab[0][0].taille
          for tableau in self.tab :
               self.temps = max(max(tab.temps for tab in tableau),self.temps)
               self.taille_min_tableau = min(min(tab.taille for tab in tableau),self.taille_min_tableau)
               self.taille_max_tableau = max(max(tab.taille for tab in tableau),self.taille_max_tableau)
          self.temps_par_pixel = self.temps / 750
          self.taille_par_pixel = (self.taille_max_tableau - self.taille_min_tableau) / 880
          self.temp_theorique_operation = 2.2e-07


if __name__ == "__main__" :
     c = Courbe()
     c.interface()

