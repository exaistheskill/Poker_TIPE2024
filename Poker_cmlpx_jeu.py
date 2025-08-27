
from Poker_cmplx_fct_jeu import *
from Poker_test_algo import *
from poker_fct_entrainement_V2 import *
from numpy.random import choice as chv



def equilibrage_main_PL(j, tour, p1, p2, flop):
    """
    Gère un tour de mise entre le joueur humain et le bot.
    - Utilise `choix_action()` pour prendre les décisions.
    - Suit les règles de check, raise, all-in et fold.
    """

    def equilibrage_aux_PL(tour, p1, p2, flop):
        print(f"\nTour de {p1.name}")

        # Le joueur (humain ou bot) choisit son action
        decision_p1 = p1.choix_action(tour, flop)
        print(f"{p1.name} a voulu joué {decision_p1}")
        nouvelle_action = min(decision_p1, p1.jeton)  # Ne pas dépasser les jetons restants
        print(f"{p1.name} a joué {nouvelle_action}")

        # Mise à jour des historiques
        p1.actions_history[tour - 1][0].append(nouvelle_action)
        p2.actions_history[tour - 1][1].append(nouvelle_action)
        p1.jeton -= nouvelle_action  # Réduire les jetons de p1 du montant misé
        
        # Comparaison des mises pour décider du prochain mouvement
        total_p1 = sum(p1.actions_history[tour - 1][0])
        total_p2 = sum(p2.actions_history[tour - 1][0])

        if total_p1 < total_p2:
            if p1.jeton == 0:
                print(f"{p1.name} a donc all-in !")
                p1.is_all_in = True
                p1.is_check = False
                p2.is_check = False

                # Ajustement des mises et retour des jetons excédentaires
                difference = total_p2 - total_p1
                p2.jeton += difference
                p2.actions_history[tour - 1][0][-1] -= difference
                p1.actions_history[tour - 1][1][-1] -= difference
                return

            print(f"{p1.name} a donc fold !")
            p1.is_fold = True
            p1.is_check = False
            p2.is_check = False
            return

        elif total_p1 == total_p2:
            # Vérifier si c'est un check
            if p1.actions_history[tour - 1][0][-1] == 0 and not p2.is_check:
                p1.is_check = True
                print(f"{p1.name} a check")
                equilibrage_aux_PL(tour, p2, p1, flop)  # L'adversaire peut réagir
            return  # Aucune relance, le tour est équilibré

        else:
            print(f"{p1.name} a raise !")
            p1.is_check = False
            p2.is_check = False
            return equilibrage_aux_PL(tour, p2, p1, flop)  # L'adversaire doit répondre

    # Déterminer qui commence le tour en fonction de `j`
    if j % 2 == 0:
        equilibrage_aux_PL(tour, p1, p2, flop)
    else:
        equilibrage_aux_PL(tour, p2, p1, flop)

def jouer_partie_PL(j, tour, p1, p2, flop, pot):
    """
    Gère un tour complet de la partie, en ajustant les mises des joueurs.
    """
    print(f"\nDébut du tour {tour}")
    
    # Équilibrer la manche avec les décisions des joueurs
    equilibrage_main_PL(j, tour, p1, p2, flop)

    # Mise à jour du pot
    pot += sum(p1.actions_history[tour - 1][0]) + sum(p2.actions_history[tour - 1][0])
    
    return pot


def commencer_jeu(fichier_strat):
    """
    Initialise une partie entre un joueur humain et un bot entraîné.
    - Charge la stratégie du bot depuis un fichier.
    - Joue des manches jusqu'à ce qu'un des joueurs perde tous ses jetons.
    """

    j = 0
    humain = PokerBot(StrategyManager(), 'humain')
    strat_bot = load_strategy(fichier_strat)
    bot = PokerBot(strat_bot, "bot")  # Chargement de la stratégie du bot

    while bot.jeton > 0 and humain.jeton > 0:
        # Mise en place d'une nouvelle partie
        jeu = init_jeu(bot, humain)
        flop = jeu[2]
        P1 = jeu[1]  # Cartes du joueur humain

        print("\n=== Nouvelle Partie ===")
        print(f"Votre main : {P1}")
        print(f"Vos jetons : {humain.jeton}\n")
        print(f"Les jetons de l'adversaire sont {bot.jeton}\n")
        pot = 0

        # **Tour 1 : Pré-Flop**
        print("\n>>> Tour 1 : Pré-Flop")
        pot = jouer_partie_PL(j, 1, humain, bot, flop, pot)
        print(f"\nPot après le premier tour : {pot}")

        # Vérification si la partie continue après le pré-flop
        partie_continue = not bot.is_fold and not humain.is_fold and not bot.is_all_in and not humain.is_all_in

        # **Tour 2 : Post-Flop (si nécessaire)**
        if partie_continue:
            print("\n>>> Tour 2 : Post-Flop")
            print(f"Flop révélé : {flop}\n")
            pot = jouer_partie_PL(j, 2, humain, bot, flop, pot)
            print(f"\nPot après le deuxième tour : {pot}")

        # **Détermination du gagnant et affichage des résultats**
        recomp_P1, recomp_P2 = conclusion_partie(humain, bot, flop, pot)
        gain_perte = recomp_P1

        print("\n>>> Résultat de la manche")
        print(f"Vous avez gagné/perdu : {gain_perte} jetons")
        print(f"Main du bot : {bot.main}\n")

        j += 1  # Incrémentation du compteur de parties

commencer_jeu("algo_100000")