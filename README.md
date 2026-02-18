#Projet Tri : 
Il s'agit d'un projet visant à visualiser le fonctionnement des algorithmes de tris ainsi que de comparer les compléxités pour comprendre leur importance.
Actuellement 12 algorithmes de tris sont implémentés.

##Fonctionnalité :
    +Choix entre 12 algorithmes de compléxité allant de O(n²) ( tri à bulle ) à O (n) ( tri par dénombrement ) 
    +Calcul effectué en parallèle grace au multiprocessing 
    +Représentation graphique des résultats avec comparaison aux courbes théoriques en O(n²), O(nlogn) et O (n)
    +Résultat stocké dans une dataclass
    +Sauvegarde dans des fichiers CSV, pour pouvoir faire de tests sur une plus grande échelle plus rapidement et plus précisement

##Fonctionnement :
    +config.json permet la configuration de la fenêtre d'affichage et des CSV ( emplacement et séparateur )
    +tri.py en charge de l'implémentation des tris et du renvoi des résultats
    +gestion_csv.py : crée les fichiers CSV, ajoute les données dans les CSV et récupère les données en les convertissant au bon format
    +analyse.py
        +interface utilisateur
        +effectue les calculs nécéssaires aux tracés de la courbe
        +trace les courbes

Le TEMPS_THEORIQUE_PAR_OPERATION est le temps moyen utiliser pour faire un échange dans un tableau. Déterminer en faisant le moyenne de temps de dizaines de milliers d'échanges.

##Utilisation : 
Il faut cloner le répertoire et lancer analyse.py

##Exemple d'utilisation : 
Sélectionner les tris souhaités :
    taille minimale = 10
    taille maximale = 1000
    intervalle = 10 

##Amélioration à venir : 
    +Limiter le nombre de points sur le graphe ( maximum 1 point tous les 3 pixels )
    +Pouvoir choisir quelle courbe afficher et quelle coubre cacher sur le graphe
    +Diviser les fonctionnalités de analyse.py

##Bonus :
Le dossier affichage contient le programme de visualisation des tris, il est indépendant du reste
