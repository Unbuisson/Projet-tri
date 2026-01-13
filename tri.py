import time
from dataclasses import dataclass
from typing import Callable
import sys
sys.setrecursionlimit(200000)

@dataclass
class TriResultat:
    nom: str
    taille: int
    temps: float
    comparaisons: int
    echanges: int

class Tri:
    def __init__(self):
        self.comparaisons = 0
        self.echanges = 0

        self.algorithmes = {
            1: ("Tri à bulle", self.tri_a_bulle),
            2: ("Tri pair impair", self.tri_pair_impair),
            3: ("Tri cocktail", self.tri_cocktail),
            4: ("Tri par insertion", self.tri_par_insertion),
            5: ("Tri par selection", self.tri_par_selection),
            6: ("Tri fusion", self.tri_fusion),
            7: ("Tri par tas", self.tri_par_tas),
            8: ("Tri rapide", self.tri_rapide)
        }

    def executer(self, choix, tableau):
        nom, algo = self.algorithmes[choix]
        self.comparaisons = 0
        self.echanges = 0
        copie = tableau.copy()
        debut = time.perf_counter()
        algo(copie)
        fin = time.perf_counter()
        return TriResultat(nom,len(tableau),fin - debut,self.comparaisons,self.echanges)

    def tri_a_bulle(self, tableau) :
        n = len(tableau)
        for i in range (n) :
            echange = False
            for j in range (0,(n-i-1)) :
                self.comparaisons += 1
                if ( tableau[j] > tableau[j+1]) :
                    tableau[j], tableau[j+1] = tableau[j+1], tableau[j]
                    self.echanges += 1
                    echange = True
            if not echange: 
                break

    #Recher le plus petit éléments et le met en première place
    def tri_par_selection(self, tableau) :
        n = len(tableau)
        for i in range(n-1) :
            min_index = i
            for j in range (i+1, n) :
                self.comparaisons += 1
                if (tableau[j] < tableau[min_index]) :
                    min_index = j
            self.comparaisons += 1
            if min_index != i:
                tableau[i],tableau[min_index] = tableau[min_index],tableau[i]
                self.echanges +=1

    #Comme le tri a bulle mais fait des allé retour
    def tri_cocktail(self, tableau) :
        echange = True
        debut = 0
        fin = len(tableau) - 1
        while echange:
            echange = False
            for i in range(debut, fin):
                self.comparaisons += 1
                if tableau[i] > tableau[i+1]:
                    tableau[i], tableau[i+1] = tableau[i+1], tableau[i]
                    self.echanges += 1
                    echange = True
            if not echange:
                break
            echange = False
            fin -= 1
            for i in range(fin - 1, debut - 1, -1):
                self.comparaisons += 1
                if tableau[i] > tableau[i+1]:
                    tableau[i], tableau[i+1] = tableau[i+1], tableau[i]
                    self.echanges += 1
                    echange = True
            debut += 1

    #Compare les éléments 1 a 1 mais uniquement les fait les indices de 2 en deux alternant pair et impair
    def tri_pair_impair(self, tableau) :
        trie = False
        while not trie :
            trie = True
            for i in range (0,len(tableau)-1,2) :
                self.comparaisons += 1
                if tableau[i] > tableau[i+1] :
                    tableau[i], tableau[i+1] = tableau[i+1], tableau[i]
                    self.echanges += 1 
                    trie = False

            for j in range (1,len(tableau)-1,2) :
                self.comparaisons += 1
                if tableau[j] > tableau[j+1] :
                    tableau[j], tableau[j+1] = tableau[j+1], tableau[j]
                    self.echanges += 1
                    trie = False
    
    #tri le tableau au fur et a mesure en mettant chaque élément a sa place dans la partie déja trié
    def tri_par_insertion(self, tableau) :
        for i in range(1, len(tableau)) :
            element_a_inserer = tableau[i]
            j = i -1
            
            while j >= 0:
                self.comparaisons += 1
                if tableau[j] > element_a_inserer :
                    tableau[j+1] = tableau[j]
                    self.echanges += 1
                    j -= 1
                else : 
                    break
            tableau[j+1] = element_a_inserer

    #Tri en plaçant l'élément directement a la position finale en créant des sous tableaux contenant les valeurs inférieurs et supérieurs a l'élément
    #Répète l'opération pour chaque élément
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
            self.comparaisons += 1
            if tab[j] <= pivot:
                tab[i], tab[j] = tab[j], tab[i]
                self.echanges += 1
                i += 1
        tab[i], tab[high] = tab[high], tab[i]
        self.echanges += 1
        return i


   
    #Divise les tableaux en plusieurs sous tableaux plus rapide a trié et les fusionne ensuite
    def tri_fusion(self, tab):
        self._tri_fusion(tab, 0, len(tab) - 1)

    def _tri_fusion(self, tab, left, right):
        if left < right:
            mid = (left + right) // 2
            self._tri_fusion(tab, left, mid)
            self._tri_fusion(tab, mid + 1, right)
            self._fusion(tab, left, mid, right)

    def _fusion(self, tab, left, mid, right):
        L = tab[left:mid + 1]
        R = tab[mid + 1:right + 1]

        i = j = 0
        k = left

        while i < len(L) and j < len(R):
            self.comparaisons += 1
            if L[i] <= R[j]:
                tab[k] = L[i]
                i += 1
            else:
                tab[k] = R[j]
                j += 1
            self.echanges += 1
            k += 1

        while i < len(L):
            tab[k] = L[i]
            i += 1
            k += 1
            self.echanges += 1

        while j < len(R):
            tab[k] = R[j]
            j += 1
            k += 1
            self.echanges += 1


    #Créer un arbre binaire pour organiser les valeurs puis, tri en le tableau en mettant a jour l'arbre
    def tri_par_tas(self, tableau) :
        def tamiser(arbre, noeud, taille_tas) :
            racine = noeud
            gauche = 2 * noeud + 1
            droite = 2 * noeud + 2

            self.comparaisons += 1
            if gauche < taille_tas and arbre[gauche] > arbre[racine] :
                racine = gauche

            self.comparaisons += 1
            if droite < taille_tas and arbre[droite] > arbre[racine] :
                racine = droite

            self.comparaisons += 1 
            if racine != noeud :
                arbre[noeud], arbre[racine] = arbre[racine], arbre[noeud]
                self.echanges += 1 
                tamiser(arbre, racine, taille_tas)

        for i in range (len(tableau) // 2 - 1, -1, -1) :
            tamiser(tableau, i, len(tableau))
        for i in range (len(tableau) - 1, 0, -1) :
            tableau[i], tableau[0] = tableau[0], tableau[i]
            self.echanges += 1
            tamiser(tableau, 0, i)
