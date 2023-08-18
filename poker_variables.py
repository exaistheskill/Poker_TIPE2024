import numpy as np
#Variables
regle = {"bet-fold" : 1, "fold-bet" : -1, "fold-fold" : 0, "jeton_base" : 30}
betPossible =  [i for i in range(5)]
nombreActions = len(betPossible)
nb_Tour = 2
carte_possible = ["D", "J", "Q", "K", "A"]


#Création des combi de toute les cartes possible dans une main
combi_main = []
for i in range(len(carte_possible)):
    for j in range(i, len(carte_possible)):
            combi_main.append([carte_possible[i], carte_possible[j]])

Deck = [[f"{j}{i}" for i in range(1,5)] for j in carte_possible ]
##Affin d'optimiser la comparaison entre carte, on crée un dico associant à chaque carte son symbole
##Exemple : "D1" ( dix de couleur 1) devient "D" (on oublie la couleur)
Deck_symb = {}
for i in carte_possible :
    for j in range(1,len(Deck[0]) + 1) :
        Deck_symb[f"{i}{j}"] = i
    Deck_symb[i] = i
##
poids_carte = {}
##On considère le poids suivant : D -> 1, J -> 2, Q -> 3, K -> 4, A -> 5
for i in range(len(carte_possible)) :
    poids_carte[carte_possible[i]] = i + 1
#Dico des combinaisons possibles :
combinaison= {"hauteur" : 0, "pair" : 1, "double_pair" : 2, "brelan" : 3, 
              "suite" : 4, "flush" : 5,"full" : 6, "carre" : 7,  "quinte_flush" : 8}
#Dico des combinaisons + carte
combi_main_plus = []
for i in combi_main :
    for j in combinaison :
        if i[0] != i[1] or j != "hauteur" :
            combi_main_plus.append((i, j))
