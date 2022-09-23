import numpy as np
import pygame
import numpy.random as npr

from database_cleaning import *


##############################
###     Fonctions du jeu   ###
##############################

# Fonction pour afficher la carte du monde pour le début du jeu
def init_map(x_bounds, y_bounds, window_surface, col):
    red_color = (255, 0, 0)
    green_color = (0, 255, 0)

    # Pour chaque pays/région
    for region in array_region:
        # On affiche le pays (voir la fonction plot_country ci-dessous)
        plot_country(region, window_surface, col, x_bounds, y_bounds, world=True, theta=0)

    # on affiche en rouge les pays que le joueur n'a pas trouvé
    for country_name in country_name_list_loose:
        plot_country(country_name, window_surface, red_color, x_bounds, y_bounds, world=True, theta=0)

    # a l'inverse, on affiche en vert les pays que le joueur a deviné
    for country_name in country_name_list_won:
        plot_country(country_name, window_surface, green_color, x_bounds, y_bounds, world=True, theta=0)


# Fonction pour afficher les contours d'un pays
def plot_country(region, window_surface, col, x_bounds, y_bounds, world, theta):
    db_country = dict_country[region].copy()
    d_long = 0
    d_lat = 0

    ### Traitement des coordonnées ###
    # Si on affiche tous les pays
    if world == True:

        # On convertit les coordonnées radiales (de dimension [-pi, pi]*[-pi/2, pi/2]) en coordonnées pour l'écran de
        # jeu (de dimension [0, x_bounds] et [0, y_bounds]). Le point (0, 0) de l'écran de jeu se trouve en haut à
        # gauche, on effectue donc une translation vers la droite de pi en x et on fait un produit en croix : x/2pi =
        # x_prime/x_bounds donc x_prime = x*x_bounds/2pi. Le raisonemment est analogue pour y
        db_country["long"] = (db_country["long"] + np.pi) / (2 * np.pi) * x_bounds
        db_country['lat'] = -(db_country['lat'] - (np.pi / 2)) / (np.pi) * y_bounds

    # Si on affiche un seul pays, alors
    else:
        # On convertit les coordonnées radiales en coordonnées pour l'écran de jeu (relatif aux nombres de pixels
        # x_bounds et y_bounds)
        db_country["long"] = (db_country["long"] + np.pi) / (2 * np.pi) * x_bounds
        db_country['lat'] = -(db_country['lat'] - (np.pi / 2)) / (np.pi) * y_bounds

        # on effectue la rotation (cf rotate())
        db_country["long"], db_country['lat'] = rotate(db_country["long"], db_country['lat'], theta=theta)

        # Maintenant, on veut "zoomer" et centrer le pays chosi. Pour ce faire, on stocke les distances max du pays ...
        d_long = np.absolute(max(db_country["long"]) - min(db_country["long"]))
        d_lat = np.absolute(max(db_country["lat"]) - min(db_country["lat"]))

        # on effectue une translation pour que le pays soit centré au coordonnée 0 en x, puis on effectue une
        # dilatation des coordonnées selon la longitude max du pays, puis on centre en x_bounds/2, soit le milieu
        # de l'écran de jeu
        db_country["long"] = db_country["long"] - np.mean(db_country["long"])
        db_country['long'] = db_country['long'] * (x_bounds / d_long) * 3 / 5 + x_bounds / 2

        # de meme pour les y
        db_country["lat"] = db_country["lat"] - np.mean(db_country["lat"])
        db_country['lat'] = db_country['lat'] * (y_bounds / d_lat) * 3 / 5 + y_bounds / 2

    # on concatène la longitude et la latitude pour créer la variable coord
    db_country["coord"] = db_country[["long", "lat"]].apply(tuple, axis=1)

    # On sélectionne les groupes contenu dans la région que l'on injecte dans un vecteur
    group_n = np.unique(db_country["group"])
    dict_db_country = dict()

    ### pour chaque groupe on affiche les coordonnées sur la surface d'affichage ###
    for group in group_n:
        dict_db_country[group] = db_country[db_country["group"] == group]
        db_group = dict_db_country[group]
        coords = list(db_group["coord"])
        pygame.draw.polygon(window_surface, col, coords, 0)

    return max(d_long, d_lat)


# Fonction qui tire au hasard un numéro dans les différentes régions (suivant une loi uniforme discrètes de 1 à max(region))
def pick_country():
    random_choice = npr.randint(1, n)

    # on retourne le pays associé au nombre tiré
    return dict_region[random_choice]


# fonction pour faire tourner les points selon un angle theta
def rotate(x, y, theta):
    c, s = np.cos(theta), np.sin(theta)
    j = np.matrix([[c, s], [-s, c]])
    m = np.dot(j, [x, y])

    return m.T[:, 0], m.T[:, 1]


# On tire au hasard un nombre compris entre 0 et 2 pi (selon une loi uniforme continue)
def pick_theta():
    return npr.uniform(0, 2 * np.pi)


def play1(window_surface, col, x_bounds, y_bounds):
    random_country = pick_country()
    theta = pick_theta()
    # On affiche un pays
    plot_country(random_country, window_surface, col, x_bounds, y_bounds, world=False, theta=theta)

    pygame.display.update()

    # En premier on retourne le nom du pays tiré au hasard pour l'ajouter à la liste des pays jouée
    return random_country


def haversine_d(wrong_answer, true_answer, capital=False):
    # Le nombre de pays n'est pas le même dans les deux bases de données, ci un pays n'a pas de capital dans la bdd
    # alors on prend les barycentres
    if not capital or wrong_answer not in array_region_cities or true_answer not in array_region_cities:
        db_true_answer = dict_country[true_answer].copy()
        db_wrong_answer = dict_country[wrong_answer].copy()

        r = 6370
        mean_lat_wrong = np.mean(db_wrong_answer["lat"])
        mean_long_wrong = np.mean(db_wrong_answer["long"])
        mean_lat_true = np.mean(db_true_answer["lat"])
        mean_long_true = np.mean(db_true_answer["long"])

        return 2 * r * np.arcsin(np.sqrt(
            np.sin((mean_lat_wrong - mean_lat_true) / 2) ** 2 + np.cos(mean_lat_true) * np.cos(mean_lat_wrong) * np.sin(
                (mean_long_wrong - mean_long_true) / 2) ** 2))
    else:

        db_wrong_answer = dict_country_capital[wrong_answer].copy()
        db_true_answer = dict_country_capital[true_answer].copy()

        r = 6370
        lat_wrong = float(db_wrong_answer['lat.capital'])
        long_wrong = float(db_wrong_answer['long.capital'])
        lat_true = float(db_true_answer['lat.capital'])
        long_true = float(db_true_answer['long.capital'])

        return 2 * r * np.arcsin(np.sqrt(
            np.sin((lat_wrong - lat_true) / 2) ** 2 + np.cos(lat_true) * np.cos(lat_wrong) * np.sin(
                (long_wrong - long_true) / 2) ** 2))


# Fonction qui renvoie le message à afficher selon le nombre d'erreurs que le joueur à commis
def message_to_player(wrong_answer_nb, country_name):
    # on ajoute 1 erreur au décompte
    wrong_answer_nb += 1
    won_game = True
    is_playing = True
    # on donne comme indice la première lettre
    if wrong_answer_nb == 1:
        wa_test = "Indice : La première lettre du pays est " + country_name[0]
        nb_error_text = "Première erreur"
    # on remet le pays dans le bon sens
    if wrong_answer_nb == 2:
        wa_test = "Indice : La dernière lettre du pays est " + country_name[-1]
        nb_error_text = "Seconde erreur"
    # on donne comme indice la deuxième lettre
    if wrong_answer_nb == 3:
        wa_test = "Indice : La deuxième lettre du pays est " + country_name[1]
        nb_error_text = "Troisième erreur"
    # Pour le dernier indice, on affiche le pays dans le bon sens
    if wrong_answer_nb == 4:
        wa_test = "Dernier indice : Le pays a été remis dans le bon sens :)"
        nb_error_text = "Quatrième erreur °o° "

    # le joueur a perdu, le pays est coloré en rouge dans la page de démarrage
    if wrong_answer_nb == 5:
        wa_test = ""
        nb_error_text = "Perdu :'( La bonne réponse était : " + country_name
        won_game = False
        country_name_list_loose.append(country_name)
        # Retour à la page d'acceuil
        is_playing = False

    return wrong_answer_nb, wa_test, nb_error_text, won_game, is_playing
