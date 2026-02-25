# Projet Tri : 
Il s'agit d'un projet visant à visualiser le fonctionnement des algorithmes de tris ainsi que de comparer les compléxités pour comprendre leur importance.
Actuellement 12 algorithmes de tris sont implémentés.

## Fonctionnalité :

* Choix entre 12 algorithmes de compléxité allant de O(n²) ( tri à bulle ) à O (n) ( tri par dénombrement ) 
* Calcul effectué en parallèle grace au multiprocessing 
* Représentation graphique des résultats avec comparaison aux courbes théoriques en O(n²), O(nlogn) et O (n)
* Choix de la comparaison (temps/echange/nombre de comparaison)
* Possiblité de caché/ affiché des courbes avec une option pour épaissir les courbes aux besoins
* Résultat stocké dans une dataclass
* Sauvegarde dans des fichiers CSV, pour pouvoir faire de tests sur une plus grande échelle plus rapidement et plus précisement
<img width="1297" height="926" alt="image" src="https://github.com/user-attachments/assets/e1bebe7a-347e-4209-be2d-6b7ce7b2a585" />




## Fonctionnement :

* config.json permet la configuration de la fenêtre d'affichage et des CSV ( emplacement et séparateur )
* tri.py en charge de l'implémentation des tris et du renvoi des résultats
* gestion_csv.py : crée les fichiers CSV, ajoute les données dans les CSV et récupère les données en les convertissant au bon format
* graphique.py en charge du tracer des graphiques
* interface.py en charge de l'interface de selection des tri et du lancement de ceux-ci
        

Le TEMPS_THEORIQUE_PAR_OPERATION est le temps moyen utiliser pour faire un échange dans un tableau. Déterminer en faisant le moyenne de temps de dizaines de milliers d'échanges.

## Utilisation : 
Il faut cloner le répertoire et lancer l'exécution depuis main.py

## Exemple d'utilisation : 
Sélectionner les tris souhaités,

* taille minimale = 10
* taille maximale = 1000
* intervalle = 10 

## Amélioration à venir :

* Travailler l'interface
* Configuration en direct du nombre de points sur la courbe

## Bonus :
Le dossier affichage contient le programme de visualisation des tris, il est indépendant du reste
