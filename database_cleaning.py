# Importation des packages
import pandas as pd
import numpy as np
# pygame est le package me permettant d'afficher une fenetre
# à installer avant de faire tourner le code (>>> pip install pygame)

##############################
### Traitement des données ###
##############################

### Importation et traitement du premier jeu de donnée ###



# Importation de la base de données
df = pd.read_csv(r'world.csv')

# on créer un vecteur contenant toutes les régions/pays
array_region = np.unique(df["region"])

# on associe à une région un numéro (cela sera utile pour le tirage aléatoire) à l'aide d'un dictionnaire python
dict_region = dict(enumerate(array_region.flatten(), 1))
n = len(array_region)

# On converti les coordonnées décimaux en radians définis sur [-pi, pi]*[-pi/2, pi/2]
df['lat'] = np.pi / 180 * df['lat']
df['long'] = np.pi / 180 * df['long']

# On va maintenant découper par région la base de donnnées
# Autrement dit on crée une sous-bdd pour chaque pays, le tout étant stocké dans un dictionnaire python
dict_country = dict()
for region in array_region:
    dict_country[region] = df[df["region"] == region].copy()

# Dans cette liste, on mettra les pays que le joueur a réussi à deviner
country_name_list_won = []

# Dans cette liste, on mettra les pays que le joueur n'a pas réussi à deviner
country_name_list_loose = []

country_name = ""

### Importation et traitement du second jeu de données ###

df_cities = pd.read_csv(r'world.cities.csv')

# On converti les coordonnées décimaux en radians définis sur [-pi, pi]*[-pi/2, pi/2]

df_cities['lat.capital'] = np.pi / 180 * df_cities['lat.capital']
df_cities['long.capital'] = np.pi / 180 * df_cities['long.capital']


# on crée un vecteur contenant toutes les régions/pays
array_region_cities = np.unique(df_cities["region"])
n_0 = len(array_region)

# on crée un dico auquelle on associe pour chaque pays sa capitale, et ses coordonnées associés
dict_country_capital = dict()
for region in array_region:
    dict_country_capital[region] = df_cities[df_cities["region"] == region].copy()





