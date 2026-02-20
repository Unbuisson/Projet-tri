"""
Constantes de configuration pour l'analyse des algorithmes de tri
"""
import json

with open('config.json', 'r') as f:
    config = json.load(f)

    # === INTERFACE GRAPHIQUE ===
    LARGEUR_FENETRE = config["fenetre"]["dimension"]["largeur_fenetre"]
    HAUTEUR_FENETRE = config["fenetre"]["dimension"]["hauteur_fenetre"]
    LARGEUR_INTERFACE = config["interface"]["largeur_interface"]
    HAUTEUR_INTERFACE = config["interface"]["hauteur_interface"]

    # Couleurs du canvas
    COULEUR_FOND_GRAPHE = config["fenetre"]["couleur"]["couleur_fond_graphes"]
    COULEUR_GRILLE = config["fenetre"]["couleur"]["couleur_grille"]
    COULEUR_AXES = config["fenetre"]["couleur"]["couleur_axes"]
    COULEUR_TEXTE_REPERE = config["fenetre"]["couleur"]["couleur_texte_repere"]

    # Dimensions du graphe
    MARGE_GAUCHE = config["fenetre"]["dimension_graphe"]["marge_gauche"]
    MARGE_DROITE = config["fenetre"]["dimension_graphe"]["marge_droite"] 
    MARGE_HAUTE = config["fenetre"]["dimension_graphe"]["marge_haute"]
    MARGE_BASSE = config["fenetre"]["dimension_graphe"]["marge_basse"]

    # Espacement des repères
    ESPACEMENT_VERTICAL = config["fenetre"]["graduation"]["espace_vertical"]
    ESPACEMENT_HORIZONTAL = config["fenetre"]["graduation"]["espace_horizontal"]

    # === GÉNÉRATION DE DONNÉES ===
    VALEUR_MAX_TABLEAU = config["valeur"]["valeur_max_tab"]
    LIMITE_RECURSION = config["valeur"]["limite_recursion"]

    # === CALCULS THÉORIQUES ===
    TEMPS_THEORIQUE_OPERATION = config["valeur"]["temps_theorique_operation"]

    # Emplacement légende
    ESPACEMENT_HORIZONTALE_LEGENDE = config["fenetre"]["legende"]["espace_horizontal"]
    ESPACEMENT_VERTICAL_LEGENDE = config["fenetre"]["legende"]["espace_vertical"]


    # === FICHIERS CSV ===
    DOSSIER_CSV = config["CSV"]["chemin_dossier"]
    SEPARATEUR_CSV = config["CSV"]["separateur_CSV"]

    # Fenêtre de chargement
    LARGEUR_CHARGEMENT = config["chargement"]["largeur_chargement"]
    HAUTEUR_CHARGEMENT = config["chargement"]["hauteur_chargement"]

    # Lissage 
    NOMBRE_PIXEL_ECART_MINIMUM = config["valeur"]["nombre_minimale_pixel_ecart"]