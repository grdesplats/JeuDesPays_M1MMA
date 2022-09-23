# Importation des fonctions des scripts annexes
from game_functions import *
from database_cleaning import *

pygame.init()
pygame.display.set_caption("Guess the Countryyy")

# Résolution de l'écran de jeu
x_bounds = 1379  # px
y_bounds = 816  # px
window_resolution = (x_bounds, y_bounds)

clock = pygame.time.Clock()

# Chargement de la bannière d'acceuil
# banner = pygame.image.load()

# Chargement du bouton "lancer le jeu"
play_button = pygame.image.load("launch_game.png")

# Initialisation des couleurs
blue_color = (89, 152, 255)
brown_color = (222, 184, 135)
black_color = (0, 0, 0)
red_color = (255, 0, 0)
green_color = (0, 255, 0)

color_active = pygame.Color('lightskyblue3')
base_font = pygame.font.Font(None, 32)
user_text = ''
myText = base_font.render('myText', True, black_color)

# création des rectangles in-game
input_rect = pygame.Rect(600, 680.0, 100, 30)
input_rect_cach_text = pygame.Rect(0, 730, 1800, 200)

# On crée le bouton pour lancer le jeu et on lui assigne des coordonnées
play_button = pygame.transform.scale(play_button, (400, 200))
play_button_rect = play_button.get_rect()
play_button_rect.x = (x_bounds + 1) / 3
play_button_rect.y = (y_bounds) / 1.5

# génération de la fenetre de jeu
window_surface = pygame.display.set_mode(window_resolution)

# changement de la couleur du fond d'écran en bleu
window_surface.fill(blue_color)

# booléen de l'écran d'acceuil
is_playing = False

# booléen de la boucle du jeu
done = False

print_screen = False
print_country = False

while not done:
    current_time = pygame.time.get_ticks()

    # Si le jeu a commencé
    if is_playing:

        while not print_country:
            # on affiche le  pays
            print_screen = False
            won_game = True
            window_surface.fill(blue_color)
            res = play1(window_surface, brown_color, x_bounds, y_bounds)

            # le nom du pays tiré
            country_name = res

            # on (ré)initialise le nombre d'érreur pour la manche
            wrong_answer_nb = 0
            print_country = True

        pygame.draw.rect(window_surface, color_active, input_rect)

        text_surface = base_font.render(user_text, True, (255, 255, 255))

        # render at position stated in arguments
        window_surface.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

        # set width of textfield so that text cannot get
        # outside of user's text input
        input_rect.w = max(100, text_surface.get_width() + 10)


    # Si le jeu n'a pas commencé
    else:

        while not print_screen:
            print_country = False
            window_surface.fill(blue_color)

            # Initialisation du jeu avec le bouton "Jouer"...
            window_surface.blit(play_button, play_button_rect)

            # et la carte du monde
            init_map(x_bounds, y_bounds, window_surface, brown_color)

            print_screen = True

    # pour chaque évenement effectué par le joueur (souris, clavier, ect...)
    for event in pygame.event.get():

        # Si le joueur ferme la fenetre
        if event.type == pygame.QUIT:

            # arret de la boucle principale
            done = True
            print("Fermeture du jeu")

        elif event.type == pygame.MOUSEBUTTONDOWN:

            # Si le joueur appuie sur le bouton jouer (la souris se situe au dessus du bouton)
            if play_button_rect.collidepoint(event.pos):
                # on lance une partie
                is_playing = True

        # Si le joueur appuie sur le clavier
        elif event.type == pygame.KEYDOWN:

            # Si le joueur veut se corriger (s'il appuie sur la touche supprimer)
            if event.key == pygame.K_BACKSPACE:
                # On enlève un caractère à chaque utilisation de la touche BackSpace
                user_text = user_text[:-1]

            # si le joueur appuie sur la touche entrée pendant la partie
            elif event.key == pygame.K_RETURN and is_playing:

                # si le mot écrit par le joueur est dans la liste des pays
                if user_text in array_region:

                    # si le mot écrit est le bon pays
                    if user_text == country_name:

                        text = base_font.render("Gagné :) Retour à l'écran d'acceuil ! ", True, green_color)
                        window_surface.blit(text, (520, 730))
                        # on ajoute le pays à la liste des pays trouvés (que l'on coloriera en vert sur l'écran de démarrage)
                        country_name_list_won.append(country_name)
                        # retour à la page d'acceuil
                        is_playing = False

                    # si le mot écrit n'est pas le bon
                    else:
                        # On affiche différentes informations pour le joueur en fonction du nombre d'erreurs (cf message_to_player() dans game_function.py)
                        wrong_answer_nb, wa_test, nb_error_text, won_game, is_playing = message_to_player(wrong_answer_nb, country_name)
                        if wrong_answer_nb == 4:
                            # on colorie tout l'écran en bleu
                            window_surface.fill(blue_color)
                            # on affiche le pays jouée, cette fois ci avec theta = 0
                            plot_country(country_name, window_surface, brown_color, x_bounds, y_bounds, world=False,
                                         theta=0)

                        print_time = current_time + 4000  # On affiche le texte pendant 3000 millisecondes
                        dist_capital = haversine_d(user_text, country_name, capital=True)
                        km_text = "Les capitales des pays se trouvent à " + str(
                            round(dist_capital, 2)) + " km de distance"

                        ## On fait apparaitre les différents textes à l'écran
                        km_text = base_font.render(km_text, True, black_color)
                        window_surface.blit(km_text, (480, 730))
                        wa_test = base_font.render(wa_test, True, black_color)
                        nb_error_text = base_font.render(nb_error_text, True, red_color)
                        window_surface.blit(wa_test, (480, 780))
                        window_surface.blit(nb_error_text, (480, 755))
                        pygame.display.update()
                        # on fait patienter le jeu pendant 3 secondes
                        while current_time < print_time:
                            current_time = pygame.time.get_ticks()

                        pygame.draw.rect(window_surface, blue_color, input_rect_cach_text)

                    user_text = ''

                # si le mot écrit n'est pas inscrit dans la liste des pays
                else:
                    print_time = current_time + 2000  # On affiche le texte pendant 1500 millisecondes
                    text = "-_- Ce pays ne se trouve pas dans la base de données -_-"
                    myText = base_font.render(text, True, black_color)
                    window_surface.blit(myText, (430, 730))
                    pygame.display.update()

                    # on fait patienter le jeu pendant 3 secondes
                    while current_time < print_time:
                        current_time = pygame.time.get_ticks()

                    pygame.draw.rect(window_surface, blue_color, input_rect_cach_text)

                # on réinitialise le texte écrit par le joueur
                user_text = ''

            # Si le joueur appuie sur la touche entrée pendant l'écran de démarrage
            elif event.key == pygame.K_RETURN and not is_playing:
                # on lance une partie
                is_playing = True


            else:
                # on récupere le texte écrit par le joueur
                user_text += event.unicode

    # mise à jour de l'écran
    pygame.display.update()

    # 60 frames par seconde
    clock.tick(60)
