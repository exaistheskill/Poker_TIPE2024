
from Poker_cmplx_fct_jeu import *
import numpy as np
import copy
from Poker_test_algo import *
import random
import time






class PokerBot:
    """
    Bot de poker utilisant la minimisation de regrets pour prendre des décisions.
    """
    def __init__(self, strategy_manager, name: str):
        self.strategy_manager = strategy_manager
        self.main = []  # Liste des cartes de la main
        self.jeton = regle["jeton_base"]
        # Historique des actions pour chaque tour : 
        # actions_history[tour-1] = [liste_actions_joueur, liste_actions_adversaire]
        self.actions_history = [[[], []] for _ in range(nb_Tour)]
        self.is_fold = False
        self.is_check = False
        self.is_all_in = False
        self.name = name
        self.main_PP = ""  # Clé de la main convertie en string

    def donner_carte(self, cartes: list):
        """
        Assigne les cartes à la main du bot et crée la clé string correspondante.
        """
        self.main = cartes
        self.main_PP = conv_carte_str(cartes)

    def prendre_decision(self, tour: int, flop: list, adversaire=None):
        """
        Prend une décision pour le tour donné en se basant sur la stratégie actuelle.
        Met à jour l'historique d'actions. Si 'adversaire' est fourni, 
        l'action est également enregistrée dans son historique.
        """
        key = self.create_key(tour, flop, self.actions_history)
        strategy = self.strategy_manager.get_strategy(key)
        
        # Sélection d'un indice selon la distribution de probabilité
        action_index = np.random.choice(np.arange(len(strategy)), p=strategy)
        # Le montant misé ne peut dépasser le nombre de jetons disponibles
        mise = min(action_index, self.jeton)
        self.actions_history[tour - 1][0].append(mise)
        if adversaire is not None:
            adversaire.actions_history[tour - 1][1].append(mise)

    def prendre_decision_bis(self, tour: int, flop: list):
        """
        Variante de la prise de décision qui n'actualise que l'historique interne du bot.
        """
        self.prendre_decision(tour, flop)

    def create_key(self, tour: int, flop: list, etat: list):
        """
        Crée une clé pour accéder à la stratégie selon l'état du jeu.
        Pour le bot 'former', on utilise une évaluation différente de la main.
        Pour les autres, la clé inclut la main convertie et l'historique d'actions.
        """
        if self.name == "former":
            if tour == 1:
                dernier_adversaire = etat[tour - 1][1][-1] if etat[tour - 1][1] else -1
                return (self.main_PP, dernier_adversaire)
            elif tour == 2:
                try:
                    eval_main = combinaison_jeu_ancien(self.main, flop)
                except NameError:
                    eval_main = combinaison_jeu(self.main, flop)
                dernier_adversaire = etat[tour - 1][1][-1] if etat[tour - 1][1] else -1
                return (self.main_PP, eval_main, dernier_adversaire)
        
        # Pour les autres bots
        if tour == 1:
            return (self.main_PP, conv_action_str(etat))
        elif tour == 2:
            return (self.main_PP, combinaison_jeu(self.main, flop), conv_action_str(etat))
        return self.main_PP

    def reinitialiser_total(self):
        """
        Réinitialise complètement l'état du bot pour une nouvelle partie.
        """
        self.main = []
        self.main_PP = ""
        self.jeton = regle["jeton_base"]
        self.actions_history = [[[], []] for _ in range(nb_Tour)]
        self.is_fold = False
        self.is_check = False
        self.is_all_in = False

    def reinitialiser_tour(self):
        """
        Réinitialise l'état du bot pour un nouveau tour tout en conservant les jetons.
        """
        self.main = []
        self.main_PP = ""
        self.actions_history = [[[], []] for _ in range(nb_Tour)]
        self.is_fold = False
        self.is_check = False
        self.is_all_in = False

    def copy(self, new_name: str):
        """
        Crée une copie indépendante du bot courant avec un nouveau nom.
        """
        nouveau_bot = PokerBot(self.strategy_manager, new_name)
        nouveau_bot.main = copy.deepcopy(self.main)
        nouveau_bot.main_PP = self.main_PP
        nouveau_bot.jeton = self.jeton
        nouveau_bot.actions_history = copy.deepcopy(self.actions_history)
        nouveau_bot.is_fold = False
        nouveau_bot.is_check = False
        nouveau_bot.is_all_in = False
        return nouveau_bot

    def choix_action(self, tour: int, flop: list):
        """
        Permet au bot de choisir une action en fonction de sa stratégie.
        Pour un joueur humain, demande l'entrée utilisateur.
        Pour un bot, ajuste les probabilités en fonction des jetons restants.
        """
        if self.name == 'humain':
            max_bet = min(self.jeton, 4)
            action = int(input(f"Quelle est votre décision ? (entrez un numéro entre 0 et {max_bet} correspondant à votre bet) : "))
            while action < 0 or action > max_bet:
                action = int(input(f"Entrez un numéro valide entre 0 et {max_bet} correspondant à votre bet : "))
            return action

        key = self.create_key(tour, flop, self.actions_history)
        strategy = self.strategy_manager.get_strategy(key, tour)
        # Filtrer les actions possibles selon les jetons disponibles
        actions_possibles = [i for i in betPossible if i <= self.jeton]
        # Extraire les probabilités associées
        probabilities = np.array([strategy[i] for i in actions_possibles])
        
        # Ajouter la probabilité des mises impossibles (supérieures aux jetons) à l'action maximale possible
        if len(actions_possibles) < len(betPossible):
            probabilities[-1] += sum(strategy[i] for i in range(len(actions_possibles), len(betPossible)))
        total_prob = probabilities.sum()
        probabilities = probabilities / total_prob if total_prob > 0 else np.full(len(probabilities), 1/len(probabilities))
        
        return np.random.choice(actions_possibles, p=probabilities)

# Fonctions utilitaires pour le jeu

def init_jeu(p1: PokerBot, p2: PokerBot):
    """
    Initialise le jeu pour deux joueurs en distribuant les cartes et en réinitialisant leurs états.
    """
    p1.reinitialiser_tour()
    p2.reinitialiser_tour()
    
    jeu = cree_jeu()  # Supposons que cree_jeu() distribue correctement les cartes
    p1.donner_carte(jeu[0])
    p2.donner_carte(jeu[1])
    
    return jeu

def equilibrage_main(j: int, tour: int, p1: PokerBot, p2: PokerBot, flop: list) -> None:
    """
    Permet d'équilibrer les mises entre deux joueurs pendant un tour.
    
    La fonction interne 'equilibrage_aux' gère récursivement les échanges de mise entre le joueur actif 
    et son adversaire jusqu'à ce que leurs mises soient alignées. Le paramètre 'j' détermine quel joueur 
    commence (selon j % 2).
    """
    def equilibrage_aux(tour: int, active: PokerBot, opponent: PokerBot, flop: list) -> None:
        # Le joueur actif choisit son action
        decision = active.choix_action(tour, flop)
        mise = min(decision, active.jeton)  # Ne pas dépasser le nombre de jetons disponibles
        print(f"le joueur {active.name} a joué {mise}")
        time.sleep(2)
        active.actions_history[tour - 1][0].append(mise)
        opponent.actions_history[tour - 1][1].append(mise)
        active.jeton -= mise  # Déduction de la mise
        
        # Calcul du total misé pour le tour courant
        total_active = sum(active.actions_history[tour - 1][0])
        total_opponent = sum(opponent.actions_history[tour - 1][0])
        
        if total_active < total_opponent:
            # Si le joueur actif a misé moins que l'adversaire
            if active.jeton == 0:
                # Le joueur actif est en all in
                print(f"{active.name} a all in")
                active.is_all_in = True
                active.is_check = False
                opponent.is_check = False
                diff = total_opponent - total_active
                # Rétablir l'équilibre en ajustant la dernière mise de l'adversaire
                opponent.jeton += diff
                opponent.actions_history[tour - 1][0][-1] -= diff
                active.actions_history[tour - 1][1][-1] -= diff
                return
            else:
                # Sinon, le joueur actif fold s'il ne peut pas égaler la mise adverse
                print(f"{active.name} a fold")
                active.is_fold = True
                active.is_check = False
                opponent.is_check = False
                return
        elif total_active == total_opponent:
            # Si les mises sont égales, vérifier la possibilité d'un check
            if active.actions_history[tour - 1][0][-1] == 0 and not opponent.is_check:
                print(f"{active.name} a check")
                active.is_check = True
                # Donner la parole à l'adversaire pour réagir
                equilibrage_aux(tour, opponent, active, flop)
            return
        else:
            # Si le joueur actif a misé plus que l'adversaire, continuer l'échange en inversant les rôles
            active.is_check = False
            opponent.is_check = False
            equilibrage_aux(tour, opponent, active, flop)

    # Le joueur qui commence dépend de la parité de j
    if j % 2 == 0:
        equilibrage_aux(tour, p1, p2, flop)
    else:
        equilibrage_aux(tour, p2, p1, flop)


def prendre_decision_jeu(j: int, tour: int, p1: PokerBot, p2: PokerBot, flop: list) -> None:
    """
    Ordonne aux deux joueurs de prendre leurs décisions pour un tour donné.
    
    La fonction interne 'prendre_decision_jeu_aux' fait d'abord agir le premier joueur 
    (avec une mise minimale obligatoire), puis l'adversaire, et déduit les mises du total des jetons.
    L'ordre est inversé selon la parité de j.
    """
    def prendre_decision_jeu_aux(tour: int, first: PokerBot, second: PokerBot, flop: list) -> None:
        # Le premier joueur prend sa décision en réaction à l'adversaire
        first.prendre_decision(tour, flop, second)
        # Mise minimale obligatoire (force une mise d'au moins 1)
        first.actions_history[tour - 1][0][-1] = max(1, first.actions_history[tour - 1][0][-1])
        second.actions_history[tour - 1][1][-1] = max(1, first.actions_history[tour - 1][0][-1])
        
        # Le deuxième joueur répond
        second.prendre_decision(tour, flop, first)
        
        # Déduction des mises engagées dans ce tour des jetons des joueurs
        first.jeton -= sum(first.actions_history[tour - 1][0])
        second.jeton -= sum(second.actions_history[tour - 1][0])
    
    if j % 2 == 0:
        prendre_decision_jeu_aux(tour, p1, p2, flop)
    else:
        prendre_decision_jeu_aux(tour, p2, p1, flop)


def jouer_partie(j: int, tour: int, p1: PokerBot, p2: PokerBot, flop: list, pot: int) -> int:
    """
    Joue un tour de la partie en équilibrant les mises des deux joueurs.
    
    La fonction met à jour le pot en ajoutant les mises cumulées des deux joueurs pour le tour.
    """
    print(f"Début du Tour {tour}")
    equilibrage_main(j, tour, p1, p2, flop)
    pot = sum(p1.actions_history[0][0]) + sum(p1.actions_history[0][1]) + sum(p1.actions_history[1][1]) +  sum(p1.actions_history[1][0])
    print(f"le pot est {pot}")
    time.sleep(1)
    return pot


def conclusion_partie(p1: PokerBot, p2: PokerBot, flop: list, pot: int):
    """
    Calcule les récompenses finales à la fin de la partie en fonction des actions et des mains des joueurs.
    la récompense étant la variation entre les jetons initiales et finales
    
    - Si aucun joueur ne fold, le résultat est déterminé par 'prendre_recompense'.
    - Si l'un des joueurs fold, la récompense est attribuée en conséquence.
    Les jetons sont mis à jour en fonction du gain ou de la perte.
    
    Renvoie un tuple (recompense_p1, recompense_p2).
    """
    # Calcul du total des mises de chaque joueur sur tous les tours
    total_p1 = sum(p1.actions_history[0][0]) + sum(p1.actions_history[1][0])
    total_p2 = sum(p1.actions_history[0][1]) + sum(p1.actions_history[1][1])
    if (not p1.is_fold) and (not p2.is_fold) :
        ma_recomp = prendre_recompense(pot, p1.main, p2.main, flop)
        if ma_recomp is False:  # Cas d'égalité (split pot)
            ma_recomp = 0
            en_recomp = 0
            p1.jeton += pot // 2
            p2.jeton += pot // 2
        else:
            if ma_recomp >= 0 :
                ma_recomp = total_p2
                en_recomp = -total_p2
                p1.jeton += pot
            if ma_recomp < 0  :
                ma_recomp = - total_p1
                en_recomp = total_p1
                p2.jeton += pot
    if p2.is_fold :
        ma_recomp = total_p2
        en_recomp = -total_p2
        p1.jeton += pot
    if p1.is_fold :
        ma_recomp = - total_p1
        en_recomp = total_p1
        p2.jeton += pot
    return (ma_recomp, en_recomp)

##Fonctions utiles pour le calcul des regrets

#fonction qui renvoie les etats qu'on devra rejouer afin de calculer le regret
#elle renvoie l'ensemble des états dont on doit calculer le regret, un état étant une partie d'un historique (une sorte de slicing de p.action)

from typing import Any, List

def prendre_ensembles_etats_regrets(j_relatif: int, tour: int, p1: PokerBot) -> List[Any]:
    """
    Construit l'ensemble des états (états complets) à partir de l'historique des actions de p1 pour un tour donné.
    
    Pour chaque décision (indice k) dans le tour, on construit un état partiel.
      - Si j_relatif est pair (0), on considère que p1 commence et on prend k actions pour chaque joueur.
      - Si j_relatif est impair (1), on considère que p1 répond et on prend k actions pour p1 et k+1 pour l'adversaire.
    
    Pour le tour 1, l'état complet est [état_partiel, [[], []]].
    Pour le tour 2, il est [copy.deepcopy(p1.actions_history[0]), état_partiel].
    
    :param j_relatif: 0 si c'est au joueur dont on calcule le regret de commencer, 1 sinon.
    :param tour: Numéro du tour (1 ou 2).
    :param p1: Le bot dont l'historique des actions est utilisé.
    :return: Liste des états complets pour lesquels le regret sera évalué.
    """
    etats_regrets = []
    actions_tour = p1.actions_history[tour - 1]  # actions_tour = [liste_actions_p1, liste_actions_adversaire]
    
    for k in range(len(actions_tour[0])):
        # Construction de l'état partiel en fonction de la parité de j_relatif
        if j_relatif % 2 == 0:
            etat_partiel = [
                copy.deepcopy(actions_tour[0][:k]),
                copy.deepcopy(actions_tour[1][:k])
            ]
        else:
            etat_partiel = [
                copy.deepcopy(actions_tour[0][:k]),
                copy.deepcopy(actions_tour[1][:k + 1])
            ]
        
        # Constitution de l'état complet selon le tour
        if tour == 1:
            etat_complet = [etat_partiel, [[], []]]
        else:
            etat_complet = [copy.deepcopy(p1.actions_history[0]), etat_partiel]
        
        etats_regrets.append(etat_complet)
    return etats_regrets


def regret_de_etat(j: int, tour: int, p1: PokerBot, p2: PokerBot, flop: List[str],
                    etat_complet: Any, jeton_P1: int, jeton_P2: int,
                    pot: int, recomp_initiale: float) -> None:
    """
    Calcule et met à jour le regret pour un état donné (état_complet) pour le joueur p1.
    
    Pour l'état courant, on identifie le niveau de décision (indice k) et on simule,
    pour chaque action alternative possible (différente de celle réellement prise),
    l'évolution de la partie en effectuant une simulation.
    
    La différence entre la récompense obtenue avec l'action alternative et la récompense initiale
    sert à mettre à jour le regret via le StrategyManager de p1.
    
    :param j: Indice global de la simulation.
    :param tour: Numéro du tour (1 ou 2).
    :param p1: Bot dont le regret est calculé.
    :param p2: Adversaire.
    :param flop: Liste des cartes du flop.
    :param etat_complet: État complet simulé pour ce point de décision.
    :param jeton_P1: Nombre de jetons initiaux de p1 pour la simulation.
    :param jeton_P2: Nombre de jetons initiaux de p2 pour la simulation.
    :param pot: Pot courant avant simulation.
    :param recomp_initiale: Récompense obtenue initialement lors du jeu réel.
    """
    # Déterminer le niveau de décision actuel à partir de l'état complet
    # Pour tour 1, etat_complet = [etat_partiel, [[], []]]
    # Pour tour 2, etat_complet = [actions_tour1, etat_partiel]
    current_state = etat_complet[0] if tour == 1 else etat_complet[1]
    print(f"état actuel {current_state}")
    decision_index = len(current_state[0])
    time.sleep(6)
    # Récupération de l'action réellement effectuée à ce niveau
    action_realisee = p1.actions_history[tour - 1][0][decision_index]
    print(f"l'action était {action_realisee}")
    # Définir les actions alternatives possibles
    actions_possibles = [a for a in betPossible if a <= jeton_P1 and a != action_realisee]
    
    for action_alternative in actions_possibles:
        time.sleep(2)
        print(f"voyons voir ce qui se passe si l'on joue {action_alternative}")
        # Création de copies simulées des bots pour tester l'action alternative
        time.sleep(4)
        p1_sim = p1.copy(p1.name + "_reg")
        p2_sim = p2.copy(p2.name + "_reg")
        
        # Réinitialisation des jetons pour la simulation
        p1_sim.jeton = jeton_P1
        p2_sim.jeton = jeton_P2
        
        # Affectation de l'état complet simulé à p1_sim
        p1_sim.actions_history = copy.deepcopy(etat_complet)
        # Ajout de l'action alternative pour le tour en cours
        p1_sim.actions_history[tour - 1][0].append(action_alternative)
        
        # Pour p2, on simule un échange en inversant les rôles dans l'état
        p2_sim.actions_history = [
            [copy.deepcopy(etat_complet[0][1]), copy.deepcopy(etat_complet[0][0])],
            [copy.deepcopy(etat_complet[1][1]), copy.deepcopy(etat_complet[1][0])]
        ]
        p2_sim.actions_history[tour - 1][1].append(action_alternative)
        
        # Mise à jour des jetons en fonction des mises engagées dans chaque tour
        p1_sim.jeton -= sum(p1_sim.actions_history[0][0])
        p2_sim.jeton -= sum(p2_sim.actions_history[0][0])
        if tour == 2:
            p1_sim.jeton -= sum(p1_sim.actions_history[1][0])
            p2_sim.jeton -= sum(p2_sim.actions_history[1][0])
        
        # Si p1_sim dispose encore de jetons
        if p1_sim.jeton >= 0:
            if p1_sim.jeton == 0:
                p1_sim.is_all_in = True
            # Si, à ce niveau, l'action alternative de p1 est inférieure à celle de p2,
            # on considère que p1 se serait foldé
            if (len(p2_sim.actions_history[tour - 1][0]) > 0 and 
                p1_sim.actions_history[tour - 1][0][-1] < p2_sim.actions_history[tour - 1][0][-1]):
                p1_sim.is_fold = True
                recomp_P1 = p1_sim.jeton - jeton_P1  # Pénalité associée au fold
            else:
                # Simulation de la suite de la partie avec l'action alternative
                pot_sim = jouer_partie(1, tour, p1_sim, p2_sim, flop, 0)
                if not p1_sim.is_fold and not p2_sim.is_fold and tour == 1:
                    pot_sim = jouer_partie(j, 2, p1_sim, p2_sim, flop, pot_sim)
                recomp_P1, _ = conclusion_partie(p1_sim, p2_sim, flop, pot_sim)
            
            # Génération de la clé d'état à partir de l'état complet
            key = p1.create_key(tour, flop, etat_complet)
            regret = recomp_P1 - recomp_initiale
            
            print(f"mon regret est de {regret}")
            #DEBUG
            if tour == 1 :
                p1.strategy_manager.update_regrets(key, tour, action_alternative, regret)
        


def chercher_regret(j: int, j_relatif: int, tour: int, p1: PokerBot, p2: PokerBot,
                    flop: List[str], jeton_P1: int, jeton_P2: int, recomp_initiale: float, pot: int) -> None:
    """
    Pour chaque état de décision extrait de p1, calcule le regret associé.
    
    :param j: Indice global de la simulation.
    :param j_relatif: Indice relatif (0 ou 1) pour déterminer l'ordre de décision.
    :param tour: Numéro du tour (1 ou 2).
    :param p1: Le bot pour lequel le regret est calculé.
    :param p2: L'adversaire.
    :param flop: Liste des cartes du flop.
    :param jeton_P1: Nombre de jetons initiaux de p1 pour la simulation.
    :param jeton_P2: Nombre de jetons initiaux de p2 pour la simulation.
    :param recomp_initiale: Récompense obtenue initialement lors du jeu réel.
    :param pot: Pot courant avant simulation.
    """
    etats_regrets = prendre_ensembles_etats_regrets(j_relatif, tour, p1)
    for etat_complet in etats_regrets:
        
        print(f"premier états à chercher {etat_complet}")
        time.sleep(6)
        regret_de_etat(j, tour, p1, p2, flop, etat_complet, jeton_P1, jeton_P2, pot, recomp_initiale)

            

# Vous pouvez ensuite appeler cette fonction comme cela est fait habituellement.

##test    
# p1 = pokerBot(StrategyManager())
# p2 = pokerBot(StrategyManager())
# jeu = init_jeu(p1, p2)
# print(jouer_partie(1, 2, p1, p2, jeu[2], 0))
# print(jouer_pour_regret(0, 1, p1, p2, jeu[2], 3, 20, 20))

# print(p1.is_fold, p2.is_fold)
# print(p1.action, p2.action, p1.jeton, p2.jeton, jeu,)
##


## mise en place de l'algo




def entrainer(num_parties: int, p1 : PokerBot, p2 : PokerBot) -> None:
    """
    Entraîne les bots sur un nombre de parties donné.
    
    Pour chaque partie, les bots jouent jusqu'à ce que l'un d'eux n'ait plus de jetons.
    À chaque tour, le jeu est simulé (distribution, mise, etc.), le pot est mis à jour,
    et les regrets sont calculés pour améliorer la stratégie via le StrategyManager.
    
    À la fin, le nombre de victoires (pour p2) et de défaites (pour p1) est affiché.
    
    :param num_parties: Nombre total de parties à simuler.
    """
    wins, losses = 0, 0

    for k in range(num_parties):
        if (k + 1) % 1000 == 0:
            print(f"{k+1} parties, déjà !")
        
        round_number = 0
        # Réinitialisation complète des bots pour une nouvelle partie
        p1.reinitialiser_total()
        p2.reinitialiser_total()
        
        # Tant que les deux bots disposent encore de jetons
        while p1.jeton > 0 and p2.jeton > 0:
            round_number += 1
            # Initialisation du jeu et distribution des cartes
            jeu = init_jeu(p1, p2)
            print(jeu)
            flop = jeu[2]  # Le flop se trouve à l'indice 2
            # Sauvegarde des jetons avant la partie pour la simulation des regrets
            jetons_pre_p1 = p1.jeton
            jetons_pre_p2 = p2.jeton
            pot = 0
            
            # Simulation du premier tour
            pot = jouer_partie(round_number, 1, p1, p2, flop, pot)
            pot_T1 = pot  # Pot après le tour 1
            time.sleep(6)
            # Vérifier si la partie continue (aucun fold ni all‑in)
            partie_continue = not p1.is_fold and not p2.is_fold and not p1.is_all_in and not p2.is_all_in
            if partie_continue:
                # Simulation du second tour
                pot = jouer_partie(round_number, 2, p1, p2, flop, pot)
            
            # Calcul de la récompense finale pour les deux joueurs
            recomp_P1, recomp_P2 = conclusion_partie(p1, p2, flop, pot)
            print(f"{p1.name} a gagné {recomp_P1}")
            time.sleep(10)
            
            
            
            # Calcul des regrets pour le joueur p1
            print(f"on cherche les regrets pour {p1.name}")
            chercher_regret(round_number, round_number % 2, 1, p1, p2, flop,
                            jetons_pre_p1, jetons_pre_p2, recomp_P1, 0)
            if len(p1.actions_history[1][0]) > 0:
                chercher_regret(round_number, round_number % 2, 2, p1, p2, flop,
                                jetons_pre_p1, jetons_pre_p2, recomp_P1, pot_T1)
            # Calcul des regrets pour le joueur p2
            
            chercher_regret(round_number, (round_number + 1) % 2, 1, p2, p1, flop,
                            jetons_pre_p2, jetons_pre_p1, recomp_P2, 0)
            if len(p2.actions_history[1][0]) > 0:
                chercher_regret(round_number, (round_number + 1) % 2, 2, p2, p1, flop,
                                jetons_pre_p2, jetons_pre_p1, recomp_P2, pot_T1)
        # Comptage des défaites et victoires selon le joueur qui n'a plus de jetons
        if p1.jeton <= 0:
            losses += 1
        if p2.jeton <= 0:
            wins += 1

    print(wins, losses)




def entrainer_temps(i, p1: PokerBot, p2 : PokerBot) :
    
    start_time = time.time()  # Enregistre le temps de début
    
    entrainer(i, p1, p2)  # Appel de la fonction que vous souhaitez mesurer
    
    end_time = time.time()  # Enregistre le temps de fin après l'exécution
    
    # Calcul de la durée totale de l'exécution
    execution_time = end_time - start_time
    
    print(f"Le temps d'exécution pour entrainer({i}) est de {execution_time} secondes.")
    save_strategy(p1.strategy_manager, f"algo_{i}")


def test_2_bot(fichier_strat_1, fichier_strat_2, num_parties):
    """
    Compare deux bots entraînés à partir de deux fichiers de stratégie différents.
    
    Le premier fichier (fichier_strat_1) sera la stratégie de bot1
    et le deuxième (fichier_strat_2) celle de bot2.
    
    Pour assurer la symétrie, à chaque nouvelle partie, on attribue
    aléatoirement les rôles p1 et p2 aux deux bots.
    
    La fonction simule num_parties parties et affiche le nombre de victoires
    pour chaque stratégie.
    """
    # Charger les stratégies
    strat1 = load_strategy(fichier_strat_1)
    strat2 = load_strategy(fichier_strat_2)
    print(len(strat1.nbr_reg[0]))
    print(len(strat2.nbr_reg[0]))
    # Créer deux bots avec leurs stratégies respectives
    bot1 = PokerBot(strat1, "bot1")
    bot2 = PokerBot(strat2, "bot2")
    
    wins_bot1, wins_bot2 = 0, 0

    for k in range(num_parties):
        if (k + 1) % 1000 == 0:
            print(f"{k+1} parties simulées...")

        # Pour chaque partie, on choisit aléatoirement qui sera p1 (première main)
        if random.random() < 0.5:
            p1, p2 = bot1, bot2
        else:
            p1, p2 = bot2, bot1

        # Réinitialiser complètement les deux bots pour une nouvelle partie
        p1.reinitialiser_total()
        p2.reinitialiser_total()

        while p1.jeton > 0 and p2.jeton > 0:
            # Pour chaque tour, on incrémente round_number (on peut ici utiliser round_number = 1, car la parité est moins importante)
            round_number = 1
            # Initialisation du jeu et distribution des cartes
            jeu = init_jeu(p1, p2)
            
            flop = jeu[2]  # Le flop se trouve à l'indice 2
            # Sauvegarde des jetons initiaux pour la simulation des regrets
            jetons_pre_p1 = p1.jeton
            jetons_pre_p2 = p2.jeton
            pot = 0

            # Simulation du premier tour (pré-flop)
            pot = jouer_partie(round_number, 1, p1, p2, flop, pot)
            pot_T1 = pot  # Pot après le premier tour

            # Si la partie continue (aucun fold ni all‑in)
            partie_continue = (not p1.is_fold and not p2.is_fold 
                               and not p1.is_all_in and not p2.is_all_in)
            if partie_continue:
                # Simulation du second tour (post-flop)
                pot = jouer_partie(round_number, 2, p1, p2, flop, pot)

            # Calcul de la récompense finale pour les deux joueurs
            recomp_P1, recomp_P2 = conclusion_partie(p1, p2, flop, pot)

            # Calcul des regrets pour p2
            chercher_regret(round_number, (round_number + 1) % 2, 1, p2, p1, flop,
                            jetons_pre_p2, jetons_pre_p1, recomp_P2, 0)
            if len(p2.actions_history[1][0]) > 0:
                chercher_regret(round_number, (round_number + 1) % 2, 2, p2, p1, flop,
                                jetons_pre_p2, jetons_pre_p1, recomp_P2, pot_T1)
            # Calcul des regrets pour p1
            chercher_regret(round_number, round_number % 2, 1, p1, p2, flop,
                            jetons_pre_p1, jetons_pre_p2, recomp_P1, 0)
            if len(p1.actions_history[1][0]) > 0:
                chercher_regret(round_number, round_number % 2, 2, p1, p2, flop,
                                jetons_pre_p1, jetons_pre_p2, recomp_P1, pot_T1)

        # Comptabilisation : si un bot n'a plus de jetons, l'autre gagne la partie.
        if p1.jeton <= 0:
            # p1 a perdu, donc le bot qui n'est pas p1 gagne.
            if p1 == bot1:
                wins_bot2 += 1
            else:
                wins_bot1 += 1
        if p2.jeton <= 0:
            if p2 == bot1:
                wins_bot2 += 1
            else:
                wins_bot1 += 1

    print(f"Résultats sur {num_parties} parties :")
    print(f"Bot1 (stratégie {fichier_strat_1}) a gagné : {wins_bot1} parties")
    print(f"Bot2 (stratégie {fichier_strat_2}) a gagné : {wins_bot2} parties")

def compare_strategies(strategy_manager1, strategy_manager2, nombre, tour=1):
    for k in range(nombre) :
        # Récupérer les dictionnaires de regrets pour le tour spécifié
        regrets1 = strategy_manager1.nbr_reg[tour - 1]
        regrets2 = strategy_manager2.nbr_reg[tour - 1]
        # Trouver les clés communes aux deux stratégies
        key = random.choice(list(regrets1))
        print(key)
        print(regrets1[key])
        print(regrets2[key])
    
    


if __name__ == "__main__":
    print("=== TEST INIT JEU ===")
    strat1 = load_strategy("algo_100000")
    strat2 = load_strategy("algo_200000")
    p1 = PokerBot(strat1, "bot1")
    p2 = PokerBot(strat2, "bot2")
    compare_strategies(strat1, strat2, 10)
    
    
    









