import numpy as np
from random import choice


#Fonction renvoyant un couple ("combinaison", "hauteur de la combinaison","est elle en main ou pas","hauteur totale")
#Exemple : ("pair", 3,4,"true") veut dire qu'il y a une pair de 10(T) (car le poids de T est 3), de plus elle est en main, et la plus haute carte est J
import numpy as np
import random

# Définition des constantes et dictionnaires globaux
regle = {"bet-fold": 1, "fold-bet": -1, "fold-fold": 0, "jeton_base": 20}
betPossible = list(range(5))
nombreActions = len(betPossible)
nb_Tour = 2
carte_possible = ["H", "N", "T", "J", "Q", "K", "A"]

# Création des combinaisons de toutes les cartes possibles dans une main (sans tenir compte de l'ordre)
combi_main = [[carte_possible[i], carte_possible[j]] for i in range(len(carte_possible)) for j in range(i, len(carte_possible))]

# Création du deck sous forme d'une liste de 28 cartes (7 valeurs x 4 couleurs)
# On utilise les chiffres '1'-'4' pour représenter les différentes couleurs.
Deck = [f"{val}{suit}" for val in carte_possible for suit in ['1', '2', '3', '4']]

# Dictionnaire associant à chaque carte son symbole (la valeur seule)
Deck_symb = {card: card[0] for card in Deck}
# On ajoute aussi les symboles eux-mêmes pour compatibilité
Deck_symb.update({val: val for val in carte_possible})

# Poids des cartes (H:1, N:2, ..., A:7)
poids_carte = {val: i + 1 for i, val in enumerate(carte_possible)}

# Dictionnaire de classement des combinaisons (plus le nombre est élevé, plus la main est forte)
combinaison_ranking = {
    "hauteur": 0,
    "pair": 1,
    "double_pair": 2,
    "brelan": 3,
    "suite": 4,
    "flush": 5,
    "full": 6,
    "carre": 7,
    "quinte_flush": 8
}

############################################
# 1. Évaluation de la main (combinaison_jeu)
############################################

def combinaison_jeu(main, flop):
    """
    Évalue la force d'une main en combinant les cartes privées (main) et le flop.
    Renvoie un tuple : (type_combinaison, valeur_principale, valeur_secondaire, présence_dans_main)
    """
    jeu = main + flop

    # Comptage des occurrences par rang
    rank_counts = {rank: 0 for rank in carte_possible}
    in_main = {rank: 0 for rank in carte_possible}
    for card in jeu:
        rank = Deck_symb[card]
        rank_counts[rank] += 1
    for card in main:
        rank = Deck_symb[card]
        in_main[rank] += 1

    # Regroupement des cartes par couleur
    suit_cards = {suit: [] for suit in ['1', '2', '3', '4']}
    for card in jeu:
        suit_cards[card[-1]].append(card)
    
    # Fonction pour vérifier la présence d'une suite (incluant le cas Ace-low)
    def check_straight(cards):
        # Récupérer les valeurs uniques
        values = sorted({poids_carte[Deck_symb[card]] for card in cards})
        # Ajout de la possibilité Ace-low (si A (7) est présent, le considérer comme 1)
        if poids_carte["A"] in values:
            values_with_ace_low = values + [1]
            values = sorted(set(values_with_ace_low))
        # Vérifier pour une séquence de 5 cartes consécutives
        for i in range(len(values) - 4):
            if values[i+4] - values[i] == 4:
                return True, values[i+4]  # renvoie True et la plus haute carte de la suite
        return False, 0

    # Vérifier la présence d'une flush et, le cas échéant, d'une quinte flush
    flush_cards = None
    for suit, cards in suit_cards.items():
        if len(cards) >= 5:
            # On trie les cartes de cette couleur par leur poids
            flush_cards = sorted(cards, key=lambda card: poids_carte[Deck_symb[card]], reverse=True)
            break  # On considère la première flush détectée

    if flush_cards:
        sf_found, sf_high = check_straight(flush_cards)
        if sf_found:
            # Retourner la quinte flush
            # On prend ici comme kicker la deuxième carte de la flush triée
            from_main = any(card in main for card in flush_cards[:5])
            return ("quinte_flush", sf_high, poids_carte[Deck_symb[flush_cards[1]]], from_main)
    
    # Évaluation du carré (4 cartes identiques)
    for rank, count in rank_counts.items():
        if count == 4:
            # Kicker : la carte la plus haute hors du carré
            kicker = max((poids_carte[r] for r in carte_possible if r != rank and rank_counts[r] > 0), default=0)
            from_main = in_main[rank] > 0
            return ("carre", poids_carte[rank], kicker, from_main)
    
    # Évaluation du full house (brelan + paire)
    three_ranks = [rank for rank, count in rank_counts.items() if count >= 3]
    pair_ranks = [rank for rank, count in rank_counts.items() if count >= 2]
    if three_ranks:
        # On choisit le brelan de plus haute valeur
        triple = max(three_ranks, key=lambda r: poids_carte[r])
        remaining_pairs = [r for r in pair_ranks if r != triple]
        if remaining_pairs:
            pair = max(remaining_pairs, key=lambda r: poids_carte[r])
            from_main = (in_main[triple] > 0) or (in_main[pair] > 0)
            return ("full", poids_carte[triple], poids_carte[pair], from_main)
    
    # Évaluation de la flush (si présente)
    if flush_cards:
        kicker1 = poids_carte[Deck_symb[flush_cards[0]]]
        kicker2 = poids_carte[Deck_symb[flush_cards[1]]]
        from_main = any(card in main for card in flush_cards[:5])
        return ("flush", kicker1, kicker2, from_main)
    
    # Évaluation de la suite (straight) sur l'ensemble des cartes
    straight_found, straight_high = check_straight(jeu)
    if straight_found:
        # On estime le kicker comme la carte juste inférieure (cette valeur est indicative)
        kicker = straight_high - 1
        from_main = any(card in main for card in jeu if (poids_carte[Deck_symb[card]] in range(straight_high-4, straight_high+1)))
        return ("suite", straight_high, kicker, from_main)
    
    # Évaluation du brelan (3 cartes identiques)
    for rank, count in rank_counts.items():
        if count == 3:
            kicker = max((poids_carte[r] for r in carte_possible if r != rank and rank_counts[r] > 0), default=0)
            from_main = in_main[rank] > 0
            return ("brelan", poids_carte[rank], kicker, from_main)
    
    # Évaluation de la double paire
    pairs = [rank for rank, count in rank_counts.items() if count == 2]
    if len(pairs) >= 2:
        pairs = sorted(pairs, key=lambda r: poids_carte[r], reverse=True)
        from_main = any(in_main[r] > 0 for r in pairs[:2])
        return ("double_pair", poids_carte[pairs[0]], poids_carte[pairs[1]], from_main)
    
    # Évaluation de la paire
    if pairs:
        pair = max(pairs, key=lambda r: poids_carte[r])
        kicker = max((poids_carte[r] for r in carte_possible if r != pair and rank_counts[r] > 0), default=0)
        from_main = in_main[pair] > 0
        return ("pair", poids_carte[pair], kicker, from_main)
    
    # Sinon, la hauteur (high card)
    sorted_jeu = sorted(jeu, key=lambda card: poids_carte[Deck_symb[card]], reverse=True)
    high1 = poids_carte[Deck_symb[sorted_jeu[0]]]
    high2 = poids_carte[Deck_symb[sorted_jeu[1]]] if len(sorted_jeu) > 1 else high1
    from_main = any(card in main for card in sorted_jeu[:2])
    return ("hauteur", high1, high2, from_main)


############################################
# 2. Fonctions de calcul de poids
############################################

def poids_main(main):
    """Retourne la somme des poids des cartes de la main."""
    return sum(poids_carte[Deck_symb[card]] for card in main)

def poids_flop(flop):
    """Retourne la somme des poids des cartes du flop."""
    return sum(poids_carte[Deck_symb[card]] for card in flop)


############################################
# 3. Distribution et création d'un jeu
############################################

def distribuer_cartes(deck, cartes_distribuees, nombre):
    """
    Distribue 'nombre' de cartes aléatoires depuis 'deck' sans répétition.
    Utilise un deck aplati pour une distribution uniforme.
    """
    # On crée une liste des cartes non distribuées
    deck_non_distribue = [card for card in deck if card not in cartes_distribuees]
    cartes = random.sample(deck_non_distribue, nombre)
    cartes_distribuees.update(cartes)
    return cartes

def cree_jeu():
    """
    Distribue un jeu complet :
      - 2 cartes pour le joueur 1
      - 2 cartes pour le joueur 2
      - 3 cartes pour le flop
    Renvoie un triplet (P1, P2, flop).
    """
    cartes_distribuees = set()
    P1 = distribuer_cartes(Deck, cartes_distribuees, 2)
    P2 = distribuer_cartes(Deck, cartes_distribuees, 2)
    flop = distribuer_cartes(Deck, cartes_distribuees, 3)
    return (P1, P2, flop)

def cree_jeu_truque(cartes_fixees):
    """
    Crée un jeu où la main du joueur 2 est fixée (pour tester des scénarios précis).
    'cartes_fixees' est une liste de 2 cartes prédéfinies pour le joueur 2.
    """
    cartes_distribuees = set(cartes_fixees)
    # Joueur 1 reçoit 2 cartes aléatoires
    P1 = distribuer_cartes(Deck, cartes_distribuees, 2)
    P2 = cartes_fixees
    flop = distribuer_cartes(Deck, cartes_distribuees, 3)
    return (P1, P2, flop)


############################################
# 4. Conversion et formatage
############################################

def conv_carte_str(main):
    """
    Convertit une main (liste de cartes) en une chaîne triée par valeur.
    Exemple : ["A1", "H3"] -> "AH"
    """
    sorted_main = sorted(main, key=lambda card: poids_carte[card[0]])
    return ''.join(card[0] for card in sorted_main)

def conv_action_str(action):
    """
    Convertit une action (liste d'actions pour P1 et P2) en une chaîne formatée.
    Exemple : [[1, 2], [0, 3]] -> "//P1:.1..2.//P2:.0..3."
    """
    out = f"//P1:{'.'.join(str(a) for a in action[0])}"
    out += f"//P2:{'.'.join(str(a) for a in action[1])}"
    return out

def listes_to_tuples(liste):
    """
    Convertit récursivement une liste (ou des listes imbriquées) en tuples.
    Utile pour obtenir des structures immuables.
    """
    return tuple(listes_to_tuples(x) if isinstance(x, list) else x for x in liste)


############################################
# 5. Stratégie et prise de décision via CFR+
############################################

def chv(options, p):
    """
    Fonction d'aide pour sélectionner une action parmi 'options' selon la distribution de probabilités 'p'.
    """
    return np.random.choice(options, p=p)

def prendre_strategie(regrets):
    """
    Applique CFR+ en utilisant le clipping des regrets négatifs.
    Renvoie une stratégie (vecteur de probabilités) pour les actions.
    """
    # On met à zéro les regrets négatifs
    regrets_positifs = np.clip(regrets, a_min=0, a_max=1e20)
    somme = np.sum(regrets_positifs)
    if somme > 0:
        return regrets_positifs / somme
    else:
        return np.full(len(regrets), 1 / len(regrets))

def prendre_strategie_new(regrets):
    """
    Variante alternative de mise à jour de la stratégie.
    Ici, si des regrets négatifs existent, on les compense en ajoutant la valeur absolue maximale.
    """
    regrets_adjust = regrets.copy()
    if np.any(regrets < 0):
        max_abs = np.max(np.abs(regrets))
        regrets_adjust += max_abs
    somme = np.sum(regrets_adjust)
    if somme > 0:
        return regrets_adjust / somme
    else:
        return np.full(len(regrets), 1 / len(regrets))

def prendre_strategie_moyenne(strategies_cumulees):
    """
    Calcule la stratégie moyenne à partir des stratégies cumulées.
    """
    strategies_positives = np.clip(strategies_cumulees, a_min=0, a_max=None)
    somme = np.sum(strategies_positives)
    if somme > 0:
        return strategies_positives / somme
    else:
        return np.full(len(strategies_cumulees), 1 / len(strategies_cumulees))

def prendre_decision(strategie):
    """
    Sélectionne une action en fonction de la stratégie (distribution de probabilité).
    """
    return chv(betPossible, p=strategie)


############################################
# 6. Calcul de la récompense
############################################

def prendre_recompense(pot, ma_main, en_main, flop):
    """
    Compare les mains des deux joueurs et renvoie :
      - pot si le joueur 1 gagne,
      - -pot si le joueur 1 perd,
      - False en cas d'égalité.
    La comparaison s'effectue selon l'ordre défini dans 'combinaison_ranking'.
    """
    combi_P1 = combinaison_jeu(ma_main, flop)
    combi_P2 = combinaison_jeu(en_main, flop)
    
    # Comparaison par catégorie de main
    if combinaison_ranking[combi_P1[0]] > combinaison_ranking[combi_P2[0]]:
        return pot
    elif combinaison_ranking[combi_P1[0]] < combinaison_ranking[combi_P2[0]]:
        return -pot
    else:
        # En cas d'égalité de catégorie, comparer les valeurs (kickers)
        if combi_P1[1] > combi_P2[1]:
            return pot
        elif combi_P1[1] < combi_P2[1]:
            return -pot
        else:
            if combi_P1[2] > combi_P2[2]:
                return pot
            elif combi_P1[2] < combi_P2[2]:
                return -pot
            else:
                return False

############################################
# Exemple d'utilisation
############################################

if __name__ == "__main__":
    print("lol")
    # # Création d'un jeu aléatoire
    # P1, P2, flop = cree_jeu()
    # print("Main joueur 1 :", P1)
    # print("Main joueur 2 :", P2)
    # print("Flop :", flop)
    
    # # Évaluation des mains
    # combi1 = combinaison_jeu(P1, flop)
    # combi2 = combinaison_jeu(P2, flop)
    # print("Combinaison joueur 1 :", combi1)
    # print("Combinaison joueur 2 :", combi2)
    
    # # Exemple de stratégie CFR+
    # regrets = np.array([0.5, -0.2, 0.1, 0.0, 0.3])
    # strat = prendre_strategie(regrets)
    # print("Stratégie obtenue :", strat)
    
    # # Décision prise selon la stratégie
    # decision = prendre_decision(strat)
    # print("Action choisie :", decision)
    
    # # Calcul de la récompense
    # pot = 20
    # recompense = prendre_recompense(pot, P1, P2, flop)
    # print("Récompense :", recompense)