import time
from dataclasses import dataclass
from typing import Callable
import sys
from constante import LIMITE_RECURSION
sys.setrecursionlimit(LIMITE_RECURSION)

@dataclass
class TriResultat:
    nom: str
    taille: int
    temps: float
    comparaisons: int
    echanges: int
    couleur : str

class Tri:
    def __init__(self):
        self.comparaisons = 0
        self.echanges = 0

        self.algorithmes : dict[int, tuple[str,str, Callable[[list[int]], None]]]= {
            1: ("Tri a bulle","#EECC66", self.tri_a_bulle),
            2: ("Tri pair impair","#EE99AA", self.tri_pair_impair),
            3: ("Tri cocktail","#6699CC", self.tri_cocktail),
            4: ("Tri par insertion","#997700", self.tri_par_insertion),
            5: ("Tri par selection","#994455", self.tri_par_selection),
            6: ("Tri fusion","#004488", self.tri_fusion),
            7: ("Tri par tas","#FDE725", self.tri_par_tas),
            8: ("Tri rapide","#5EC962", self.tri_rapide),
            9: ("Tri a peigne","#21918C",self.tri_a_peigne),
            10: ("Tri de Shell","#C77DFF", self.tri_de_shell),
            11: ("Tri par denombrement","#FF6F61", self.tri_par_denombrement),
            12: ("Tri par seaux","#2EC4B6", self.tri_par_seaux)

        }

    def executer(self, choix : int, tableau : list[int]) -> TriResultat:
        """Execute le tri demande et renvoie les statistique de celui ci au format TriResultat"""
        nom, couleur, algo = self.algorithmes[choix]
        self.comparaisons = 0
        self.echanges = 0
        copie = tableau.copy()
        debut = time.perf_counter()
        algo(copie)
        fin = time.perf_counter()
        return TriResultat(nom ,len(tableau),fin - debut,self.comparaisons,self.echanges,couleur)

    def tri_a_bulle(self, tableau):
        """Compare les éléments 1 à 1 et les intervertis s'ils sont dans le mauvaise ordre"""
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


    def tri_par_selection(self, tableau):
        """Trouve le plus petit élément du tableaux et le met en première position"""
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


    def tri_cocktail(self, tableau):
        """Fonctionne comme le tri a bulle mais parcour le tableau dans les deux sens"""
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


    def tri_pair_impair(self, tableau):
        """ Compare les éléments 1 a 1 mais uniquement les fait les indices de 2 en deux alternant pair et impair"""
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
    
    def tri_par_insertion(self, tableau):
        """tri le tableau au fur et a mesure en mettant chaque élément a sa place dans la partie déja trié"""
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


    def tri_rapide(self, tab) :
        """
        Tri en plaçant l'élément directement a la position finale en créant des sous tableaux contenant les valeurs inférieurs et supérieurs a l'élément
        Répète l'opération pour chaque élément
        """
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


   
    def tri_fusion(self, tab):
        """Divise les tableaux en plusieurs sous tableaux plus rapide a trié et les fusionne ensuite"""
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


    def tri_par_tas(self, tableau) :
        """Créer un arbre binaire pour organiser les valeurs puis, tri en le tableau en mettant a jour l'arbre"""
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
    

    def tri_a_peigne(self,tableau) :
        intervalle = len(tableau)
        echange = True
        while intervalle > 1 or echange :
            intervalle = int((intervalle/1.3))
            if intervalle < 1 :
                intervalle = 1 
            i = 0 
            echange = False
            while i <  len(tableau) - intervalle :
                self.comparaisons += 1
                if tableau[i] > tableau[i+intervalle] :
                    tableau[i], tableau[i+intervalle] = tableau[i+intervalle], tableau[i]
                    self.echanges+=1
                    echange = True
                i += 1

    def tri_de_shell(self, tableau):
        n = len(tableau)
        gap = n // 2

        while gap > 0:
            for i in range(gap, n):
                temp = tableau[i]
                j = i

                while j >= gap:
                    self.comparaisons += 1
                    if tableau[j - gap] > temp:
                        tableau[j] = tableau[j - gap]
                        self.echanges += 1
                        j -= gap
                    else:
                        break

                tableau[j] = temp
            gap //= 2


    def tri_par_denombrement(self, tableau):
        if len(tableau) == 0:
            return

        max_val = max(tableau)
        min_val = min(tableau)

        plage = max_val - min_val + 1
        compteur = [0] * plage

        # Comptage
        for nombre in tableau:
            compteur[nombre - min_val] += 1
            self.echanges += 1  # On considère l'écriture comme échange

        index = 0

        # Reconstruction
        for i in range(plage):
            while compteur[i] > 0:
                self.comparaisons += 1
                tableau[index] = i + min_val
                self.echanges += 1
                index += 1
                compteur[i] -= 1

    def tri_par_seaux(self, tableau):
        if len(tableau) == 0:
            return

        min_val = min(tableau)
        max_val = max(tableau)

        bucket_count = len(tableau)
        buckets = [[] for _ in range(bucket_count)]

        # Répartition dans les seaux
        for val in tableau:
            index = int((val - min_val) / (max_val - min_val + 1) * bucket_count)
            buckets[index].append(val)
            self.echanges += 1

        # Tri de chaque seau avec insertion
        index = 0
        for bucket in buckets:
            # tri insertion local
            for i in range(1, len(bucket)):
                key = bucket[i]
                j = i - 1
                while j >= 0:
                    self.comparaisons += 1
                    if bucket[j] > key:
                        bucket[j + 1] = bucket[j]
                        self.echanges += 1
                        j -= 1
                    else:
                        break
                bucket[j + 1] = key

            # Réassemblage
            for val in bucket:
                tableau[index] = val
                self.echanges += 1
                index += 1