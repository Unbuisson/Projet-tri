import random
import time
import os
import sys

sys.setrecursionlimit(5000)

class Tri_Affichage:
    def __init__(self):
        self.operations = 0
        self.elements_parcourus = 0
        self.temps = 0
        self.supr = 0
        self.visualisation = False
        self.nom_tri = [
    "tri bogo","tri Staline","tri a bulle", "tri par selection",
    "tri cocktail", "tri rapide", "tri fusion", "tri pair impair",
    "tri par insertion", "tri par tas",
    "tri de shell", "tri par denombrement", "tri par seaux"
    ]

    def getNom_Tri(self) :
        return self.nom_tri


    def reset_compteurs(self):
        self.operations = 0
        self.elements_parcourus = 0
        self.temps = 0
        self.supr = 0

    #Fonction lançant les tris et renvoyant tout les opérations nécéssaires
    def effectuer_tri(self,choix = int, affichage = bool, tableau = list) :
        self.reset_compteurs()
        self.visualisation = False
        dic = {
            1 : self.tri_bogo,
            2 : self.tri_staline,
            3 : self.tri_a_bulle,
            4 : self.tri_par_selection,
            5 : self.tri_cocktail,
            6 : self.tri_rapide,
            7 : self.tri_fusion,
            8 : self.tri_pair_impair,
            9 : self.tri_par_insertion,
            10 : self.tri_par_tas,
            11 : self.tri_de_shell,
            12 : self.tri_par_denombrement,
            13 : self.tri_par_seaux
        }
        if affichage :
            tab = list(tableau)
        self.temps = time.time()
        dic[choix](tableau)
        self.temps = time.time() - self.temps
        result = [self.nom_tri[choix-1],len(tableau),self.temps,self.elements_parcourus,self.operations]
        if affichage :
            self.reset_compteurs()
            self.visualisation = True
            if choix == 7 :
                self.tri_fusion_affichage(tab)
                result = [self.nom_tri[choix-1],len(tableau),self.temps,self.elements_parcourus,self.operations]
            elif choix == 6:
                self.tri_rapide_affichage(tab)
                result = [self.nom_tri[choix-1],len(tableau),self.temps,self.elements_parcourus,self.operations]
            else : 
                dic[choix](tab)
        self.afficher_resultat()
        return result
    
    def afficher_resultat(self) :
        def taille_voulu(mot) :
            while len(mot) < 50 :
                mot += " "
            mot += "|"
            return mot
        print('\033[36m')
        print(" ---------------Résultat--------------------------")
        print(taille_voulu(f"|nombre d'élément parcourus : {self.elements_parcourus}"))
        print(taille_voulu(f"|nombre d'opération effectué : {self.operations}"))
        if self.supr != 0 :
            print(taille_voulu(f"|Nombre d'élément supprimer : {self.supr}"))
        print(taille_voulu(f"|Temps utilisé : {round(self.temps,4)}s"))
        print(" -------------------------------------------------")
        print('\033[0m')

    def interface(self) :
        print("Quel tri voulez-vous utiliser ?")
        print("      1 - tri bogo")
        print("      2 - tri staline")
        print("      3 - tri à bulle (bubble sort)")
        print("      4 - tri par sélection")
        print("      5 - tri cocktail")
        print("      6 - tri rapide (quick sort)")
        print("      7 - tri fusion (merge sort)")
        print("      8 - tri pair impair (odd-even sort)")
        print("      9 - tri par insertion")
        print("      10 - tri par tas (heap sort)")
        print("      11 - tri de shell")
        print("      12 - tri par dénombrement")
        print("      13 - tri par seaux")
        choix = int(input("Votre choix: "))
        print("Combien d'élément voulez vous ?")
        nombre_element = int(input("Saississez un nombre positif : "))
        print("Souhaitez vous un affichage ?")
        affichage = input("o/n :")
        if affichage == "o" :
          affichage = True
        else :
            affichage = False
        self.reset_compteurs()
        self.effectuer_tri(choix,affichage,[random.randint(0, pow(2,14)) for _ in range (nombre_element)])
        return 0


    def afficher_tableau(self, tableau, message="", index1=-1, index2=-1) :
        if not self.visualisation:
            return
        os.system("cls")
        print(f"Nombre d'element : {len(tableau)} | {message}")
        print("Tableau: [", end="")
        for i in range(0,len(tableau)):
            if index1 == i or i == index2:
                print(f'\033[33m{tableau[i]}\033[0m', end="") 
            else:
                print(f"{tableau[i]}", end="")
            if i < len(tableau) - 1:
                print(", ", end="")
        print("]")
        print(f"Éléments parcourus: {self.elements_parcourus} | Opérations: {self.operations}")
        print()
        maxi = 0
        tabTemp = list(tableau)
        print('\033[32m',end="")
        for _ in range (len(tabTemp)) :
            maxi = -1 
            for k in range(len(tabTemp)):
                if tabTemp[k] != -1:
                    maxi = k
                    break
            for i in range(len(tabTemp)) :
                if (tabTemp[i] != -1 and tabTemp[i] >= tabTemp[maxi]) :
                    maxi = i
            for i in range(0,len(tabTemp)) :
                if index1 == i or i == index2:
                    print("\033[33m",end="")
                if (tabTemp[i] != -1 ) :
                    print("   ",end="")
                else :
                    print("■■ ",end="")
                print('\033[32m',end="")
            if maxi != -1:
                tabTemp[maxi] = -1 
            print()

        #time.sleep(0.1) # Pause introduisant le temps non-algorithmique
        input()
        print("\n")
        print('\033[0m')


    #Compare les éléménts 1 a 1 et les échanges s'ils ne sont pas dans le bonne ordre
    def tri_a_bulle(self, tableau) :
        n = len(tableau)
        for i in range (n) :
            echange = False
            self.elements_parcourus += 1
            for j in range (0,(n-i-1)) :
                self.elements_parcourus += 1 
                if ( tableau[j] > tableau[j+1]) :
                    tableau[j], tableau[j+1] = tableau[j+1], tableau[j]
                    self.operations += 3 
                    echange = True
                self.afficher_tableau(tableau, f"Tri à bulle - i={i}, j={j}",j+1)
            if not echange: 
                break
        return tableau

    #Recher le plus petit éléments et le met en première place
    def tri_par_selection(self, tableau) :
        n = len(tableau)
        for i in range(n-1) :
            self.elements_parcourus += 1
            min_index = i
            for j in range (i+1, n) :
                self.elements_parcourus += 1 
                if (tableau[j] < tableau[min_index]) :
                    min_index = j
                    self.operations += 1
            self.afficher_tableau(tableau,"Tri par sélection",min_index,i)       
            if min_index != i:
                tableau[i],tableau[min_index] = tableau[min_index],tableau[i]
                self.operations += 3
        self.afficher_tableau(tableau,"Tri par sélection")
        return tableau
    
    #Mélange le tableau et vérifie s'il est trié ou non
    def tri_bogo(self, tableau) :
        compteur = 0
        i = 0
        while True  :
            compteur += 1
            random.shuffle(tableau)
            self.operations += len(tableau)  
            self.afficher_tableau(tableau, f"Tri bogo - Essai {compteur}")
            while i < len(tableau)-1 and tableau[i] <= tableau[i+1] :
                i += 1
                self.elements_parcourus += 1
            if i == len(tableau)-1 :
                return tableau
            else :
                i = 0
    
    #Supprimer les éléments mal rangé
    def tri_staline(self, tableau) :
        i = 0
        taille = len(tableau)
        self.supr = 0
        while i < taille - 1 :
            self.elements_parcourus += 1 
            if (tableau[i] > tableau[i+1]) :
                tableau.pop(i+1)
                self.operations += len(tableau) - i
                self.supr += 1
                taille -= 1
            else :
                i += 1
                self.operations += 1
            self.afficher_tableau(tableau, f"Tri Staline - Éliminé {self.supr}",i)
        self.afficher_tableau(tableau, "Tri Staline")
        return tableau
    

    #Comme le tri a bulle mais fait des allé retour
    def tri_cocktail(self, tableau) :
        swapped = True
        start = 0
        end = len(tableau) - 1
        while swapped:
            swapped = False
            for i in range(start, end):
                self.elements_parcourus += 1
                if tableau[i] > tableau[i+1]:
                    tableau[i], tableau[i+1] = tableau[i+1], tableau[i]
                    self.operations += 3
                    swapped = True
                self.afficher_tableau(tableau, "Tri cocktail",i+1)
            if not swapped:
                break
            swapped = False
            end -= 1
            for i in range(end - 1, start - 1, -1):
                self.elements_parcourus += 1
                if tableau[i] > tableau[i+1]:
                    tableau[i], tableau[i+1] = tableau[i+1], tableau[i]
                    self.operations += 3
                    swapped = True
                self.afficher_tableau(tableau, "Tri cocktail",i)
            start += 1
        return tableau

    #Compare les éléments 1 a 1 mais uniquement les fait les indices de 2 en deux alternant pair et impair
    def tri_pair_impair(self, tableau) :
        trie = False
        while not trie :
            trie = True
            for i in range (0,len(tableau)-1,2) :
                self.afficher_tableau(tableau,"Tri pair/impair",i,i+1)
                self.elements_parcourus += 1 
                if tableau[i] > tableau[i+1] :
                    tableau[i], tableau[i+1] = tableau[i+1], tableau[i]
                    self.operations += 3 
                    trie = False
                    self.afficher_tableau(tableau,"Tri pair/impair",i,i+1)

            for j in range (1,len(tableau)-1,2) :
                self.afficher_tableau(tableau, "Tri pair/impair",j,j+1)
                self.elements_parcourus += 1 
                if tableau[j] > tableau[j+1] :
                    tableau[j], tableau[j+1] = tableau[j+1], tableau[j]
                    self.operations += 3 
                    trie = False
                    self.afficher_tableau(tableau, "Tri pair/impair",j,j+1)
                    
        self.afficher_tableau(tableau,"Tri pair/impair")
        return tableau
    
    #tri le tableau au fur et a mesure en mettant chaque élément a sa place dans la partie déja trié
    def tri_par_insertion(self, tableau) :
        n = len(tableau)
        for i in range(1, n) :
            self.elements_parcourus += 1 
            element_a_inserer = tableau[i]
            j = i 
            
            while j > 0 and tableau[j-1] > element_a_inserer :
                self.elements_parcourus += 1 
                tableau[j] = tableau[j-1] 
                self.operations += 1 
                j -= 1
                self.operations += 1
                self.afficher_tableau(tableau, "Tri insertion",i,j)
            
            tableau[j] = element_a_inserer
            self.operations += 1 
        
        self.afficher_tableau(tableau, "Tri insertion")
        return tableau

    #Tri en plaçant l'élément directement a la position finale en créant des sous tableaux contenant les valeurs inférieurs et supérieurs a l'élément
    #Répète l'opération pour chaque élément
    def tri_rapide(self,tableau) :
        if (len(tableau)<2) :
            return tableau
        tab_inf = []
        tab_sup = []
        pivot = tableau.pop(-1)
        for element in tableau :
            self.elements_parcourus += 1
            if (element < pivot) :
                tab_inf.append(element)
                self.operations += 1
            else :
                tab_sup.append(element)
                self.operations +=1
        self.operations += 1
        return self.tri_rapide(tab_inf) + [pivot] + self.tri_rapide(tab_sup)

   
    #Divise les tableaux en plusieurs sous tableaux plus rapide a trié et les fusionne ensuite
    def tri_fusion(self,tableau) :
        def tri_interne(tab1,tab2) :
            self.elements_parcourus += 2
            if len(tab1) == 0 :
                return tab2
            if len(tab2) == 0 :
                return tab1
            if ( tab1[0] < tab2[0] ) :
                self.operations += 1
                return [tab1[0]] + tri_interne(tab1[1:],tab2)
            else :
                self.operations += 1
                return [tab2[0]] + tri_interne(tab1,tab2[1:])
            
        if (len(tableau) <= 1 ) :
            return tableau
        else :
            return tri_interne(self.tri_fusion(tableau[:(int(len(tableau)/2))]),self.tri_fusion(tableau[(int(len(tableau)/2)):]) )

    #Créer un arbre binaire pour organiser les valeurs puis, tri en le tableau en mettant a jour l'arbre
    def tri_par_tas(self, tableau) :
        n = len(tableau) 
        def tamiser(arbre, noeud, taille_tas) :
            racine = noeud
            gauche = 2 * noeud + 1
            droite = 2 * noeud + 2
            self.elements_parcourus += 1 
            if gauche < taille_tas and arbre[gauche] > arbre[racine] :
                racine = gauche
                self.operations += 1 
            if droite < taille_tas and arbre[droite] > arbre[racine] :
                racine = droite
                self.operations += 1 
            if racine != noeud :
                arbre[noeud], arbre[racine] = arbre[racine], arbre[noeud]
                self.operations += 3
                self.afficher_tableau(arbre, "Tri par Tas",noeud,racine)
                tamiser(arbre, racine, taille_tas)
        for i in range (n // 2 - 1, -1, -1) :
            self.operations += 1
            tamiser(tableau, i, n)
        for i in range (n - 1, 0, -1) :
            tableau[i], tableau[0] = tableau[0], tableau[i]
            self.operations += 3
            self.afficher_tableau(tableau, "Tri par Tas",0,i)
            
            tamiser(tableau, 0, i)
        
        self.afficher_tableau(tableau, f"Tri par Tas")
        return tableau


    #Code généré par IA pour gérer l'affichage des tableaux utilisant des sous tableaux
    def _partition(self, tableau, low, high):
        pivot = tableau[high]
        i = low - 1
        self.operations += 1
        
        self.afficher_tableau(tableau, f"Tri Rapide - Partitionnement [{low}-{high}] (Pivot: {pivot})", high) # High est l'indice du pivot

        for j in range(low, high):
            self.elements_parcourus += 1
            if tableau[j] <= pivot:
                i = i + 1
                tableau[i], tableau[j] = tableau[j], tableau[i]
                self.operations += 3 
                self.afficher_tableau(tableau, f"Tri Rapide - Swap (Pivot: {pivot})", i, j)
        
        # Place le pivot à sa position correcte
        tableau[i + 1], tableau[high] = tableau[high], tableau[i + 1]
        self.operations += 3
        self.afficher_tableau(tableau, f"Tri Rapide - Placement du Pivot ({pivot})", i + 1, high)
        
        return i + 1

    def _tri_rapide_recursif(self, tableau, low, high):
        if low < high:
            self.operations += 1
            pivot_index = self._partition(tableau, low, high)
            
            # Appel récursif sur les sous-tableaux
            self._tri_rapide_recursif(tableau, low, pivot_index - 1)
            self._tri_rapide_recursif(tableau, pivot_index + 1, high)

    def tri_rapide_affichage(self, tableau):
        self._tri_rapide_recursif(tableau, 0, len(tableau) - 1)
        self.afficher_tableau(tableau, f"Tri Rapide - Terminé")
        return tableau
    
    def _fusion(self, tableau, low, mid, high):
        left = tableau[low:mid + 1]
        right = tableau[mid + 1:high + 1]
        
        i = j = 0
        k = low
        

        while i < len(left) and j < len(right):
            self.elements_parcourus += 1
            if left[i] <= right[j]:
                tableau[k] = left[i]
                i += 1
            else:
                tableau[k] = right[j]
                j += 1
            self.operations += 2 # Affectation et Incrémentation de k
            k += 1
            self.afficher_tableau(tableau, f"Tri Fusion - Début Fusion [{low}-{high}]", i, j)
        # Copie des éléments restants
        while i < len(left):
            self.elements_parcourus += 1
            tableau[k] = left[i]
            i += 1
            k += 1
            self.operations += 2
        
        while j < len(right):
            self.elements_parcourus += 1
            tableau[k] = right[j]
            j += 1
            k += 1
            self.operations += 2

        self.afficher_tableau(tableau, f"Tri Fusion - Fin Fusion [{low}-{high}]", low, high)


    def _tri_fusion_recursif(self, tableau, low, high):
        if low < high:
            self.operations += 1
            mid = (low + high) // 2
            
            self.afficher_tableau(tableau, f"Tri Fusion - Division [{low}-{high}]", low, high)

            self._tri_fusion_recursif(tableau, low, mid)
            self._tri_fusion_recursif(tableau, mid + 1, high)
            
            self._fusion(tableau, low, mid, high)


    def tri_fusion_affichage(self, tableau):
        self._tri_fusion_recursif(tableau, 0, len(tableau) - 1)
        self.afficher_tableau(tableau, f"Tri Fusion - Terminé")
        return tableau


    def tri_de_shell(self, tableau):
        n = len(tableau)
        gap = n // 2

        while gap > 0:
            for i in range(gap, n):
                self.elements_parcourus += 1
                temp = tableau[i]
                j = i

                while j >= gap:
                    self.elements_parcourus += 1
                    if tableau[j - gap] > temp:
                        tableau[j] = tableau[j - gap]
                        self.operations += 1
                        j -= gap
                        self.afficher_tableau(tableau, "Tri de Shell", j, j-gap)
                    else:
                        break

                tableau[j] = temp
                self.operations += 1

            gap //= 2

        self.afficher_tableau(tableau, "Tri de Shell - Terminé")
        return tableau
    
    def tri_par_denombrement(self, tableau):
        if len(tableau) == 0:
            return tableau

        min_val = min(tableau)
        max_val = max(tableau)

        plage = max_val - min_val + 1
        compteur = [0] * plage

        # Comptage
        for val in tableau:
            self.elements_parcourus += 1
            compteur[val - min_val] += 1
            self.operations += 1

        index = 0

        # Reconstruction
        for i in range(plage):
            while compteur[i] > 0:
                self.elements_parcourus += 1
                tableau[index] = i + min_val
                self.operations += 1
                compteur[i] -= 1
                index += 1
                self.afficher_tableau(tableau, "Tri par Dénombrement", index-1)

        self.afficher_tableau(tableau, "Tri par Dénombrement - Terminé")
        return tableau
    


    def tri_par_seaux(self, tableau):
        if len(tableau) == 0:
            return tableau

        min_val = min(tableau)
        max_val = max(tableau)
        n = len(tableau)

        buckets = [[] for _ in range(n)]

        # Répartition
        for val in tableau:
            self.elements_parcourus += 1
            index = int((val - min_val) / (max_val - min_val + 1) * n)
            buckets[index].append(val)
            self.operations += 1

        index = 0

        # Tri insertion dans chaque seau
        for bucket in buckets:
            for i in range(1, len(bucket)):
                key = bucket[i]
                j = i - 1

                while j >= 0:
                    self.elements_parcourus += 1
                    if bucket[j] > key:
                        bucket[j+1] = bucket[j]
                        self.operations += 1
                        j -= 1
                    else:
                        break

                bucket[j+1] = key
                self.operations += 1

            # Remise dans le tableau principal
            for val in bucket:
                tableau[index] = val
                self.operations += 1
                self.afficher_tableau(tableau, "Tri par Seaux", index)
                index += 1

        self.afficher_tableau(tableau, "Tri par Seaux - Terminé")
        return tableau


if __name__ == "__main__" :
    t = Tri_Affichage()
    t.interface()