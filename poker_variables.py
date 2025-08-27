import numpy as np
import random
# Variables
regle = {"jeton_base" : 20}
betPossible =  [i for i in range(5)]
nombreActions = len(betPossible)
nb_Tour = 2
carte_possible = ["H","N","T", "J", "Q", "K", "A"]

# Création des combi de toutes les cartes possibles dans une main
combi_main = [[carte_possible[i], carte_possible[j]] for i in range(len(carte_possible)) for j in range(i, len(carte_possible))]

Deck = [[f"{j}{i}" for i in range(1,5)] for j in carte_possible]

# Optimisation de la comparaison entre carte, on crée un dico associant à chaque carte son symbole
Deck_symb = {f"{i}{j}": i for i in carte_possible for j in range(1,len(Deck[0]) + 1)}
Deck_symb.update({i: i for i in carte_possible})

# On considère le poids suivant : H -> 1, N -> 2, T -> 3, J -> 4, Q -> 5, K -> 6, A -> 7.
poids_carte = {carte_possible[i]: i + 1 for i in range(len(carte_possible))}

# Dico des combinaisons possibles
combinaison= {"hauteur" : 0, "pair" : 1, "double_pair" : 2, "brelan" : 3, 
              "suite" : 4, "flush" : 5,"full" : 6, "carre" : 7,  "quinte_flush" : 8}

# Dico des combinaisons + carte
combi_main_plus = [(i, j) for i in combi_main for j in combinaison if i[0] != i[1] or j != "hauteur"]



