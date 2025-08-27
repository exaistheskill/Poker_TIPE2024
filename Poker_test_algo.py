
from Poker_cmplx_fct_jeu import *

import numpy as np
import os
from collections import defaultdict
import pickle 
import matplotlib.pyplot as plt

class StrategyManager:
    """
    Gestionnaire des stratégies et des regrets pour le PokerBot.
    Stocke séparément les regrets pour le premier tour (T1) et le deuxième tour (T2).
    """
    def __init__(self):
        # Initialisation des dictionnaires de regrets pour chaque tour
        self.regret_T1 = defaultdict(lambda: np.zeros(nombreActions))
        self.regret_T2 = defaultdict(lambda: np.zeros(nombreActions))
        # Regrets stockés dans une liste pour un accès par tour (index 0 pour T1, index 1 pour T2)
        self.nbr_reg = [self.regret_T1, self.regret_T2]

    def update_regrets(self, key, tour: int, action: int, regret: float) -> None:
        """
        Met à jour la valeur de regret pour une action spécifique à partir d'une clé d'état donnée.

        :param key: Clé représentant l'état de jeu (par exemple, une combinaison de cartes et d'actions).
        :param tour: Numéro du tour (1 ou 2).
        :param action: Indice de l'action pour laquelle mettre à jour le regret.
        :param regret: Valeur du regret à ajouter.
        """
        self.nbr_reg[tour - 1][key][action] += regret

    def get_strategy(self, key, tour: int = 1) -> np.ndarray:
        return prendre_strategie(self.nbr_reg[tour-1][key])

#cette partie définie des fonctions qui seront utilisés pour tester notre algo contre différentes stratégie
def save_strategy(strategy_manager, base_filename="strategy_manager.pkl"):
    """
    Sauvegarde la stratégie du StrategyManager dans un fichier pickle.
    
    La stratégie est enregistrée dans le dossier 'fichier_strat'.
    Un nom de fichier unique est généré pour éviter les collisions.
    
    :param strategy_manager: Instance de StrategyManager à sauvegarder.
    :param base_filename: Nom de base pour le fichier de sauvegarde.
    """
    directory = "fichier_strat"
    if not os.path.exists(directory):
        os.makedirs(directory)  # Crée le dossier s'il n'existe pas

    # Génération d'un nom de fichier unique
    filename = base_filename
    file_counter = 0
    filepath = os.path.join(directory, filename)
    
    while os.path.exists(filepath):
        file_counter += 1
        filename = f"{base_filename.split('.pkl')[0]}_{file_counter}.pkl"
        filepath = os.path.join(directory, filename)

    # Préparer les données à sauvegarder
    data = {
        'regret_T1': dict(strategy_manager.regret_T1),
        'regret_T2': dict(strategy_manager.regret_T2)
    }
    
    # Sauvegarder dans un fichier pickle
    with open(filepath, "wb") as f:
        pickle.dump(data, f)
    print(f"Strategy saved to {filepath}")


def load_strategy(filename):
    """
    Charge une stratégie depuis un fichier pickle et renvoie une instance de StrategyManager.
    
    Si le fichier n'existe pas ou si le contenu est invalide, affiche un message d'erreur et renvoie None.
    
    :param filename: Nom du fichier de stratégie (ex. "strategy_manager.pkl" ou "strategy_manager_1.pkl").
    :return: Instance de StrategyManager avec les regrets chargés ou None si le fichier est introuvable.
    """
    import os
    import pickle
    from collections import defaultdict
    import numpy as np

    directory = "fichier_strat"
    filepath = os.path.join(directory, filename)

    if not os.path.exists(filepath):
        print(f"No strategy file found at {filepath}")
        return None

    with open(filepath, "rb") as f:
        data = pickle.load(f)

    # Utiliser la taille de betPossible pour définir le vecteur de regrets
    try:
        num_actions = len(betPossible)
    except NameError:
        print("Erreur : la variable globale 'betPossible' n'est pas définie.")
        return None

    # S'assurer que les données chargées pour regret_T1 et regret_T2 sont des dictionnaires
    regret_T1_data = data.get('regret_T1')
    if not isinstance(regret_T1_data, dict):
        print("Attention : regret_T1 n'est pas un dictionnaire, utilisation d'un dictionnaire vide.")
        regret_T1_data = {}
    regret_T2_data = data.get('regret_T2')
    if not isinstance(regret_T2_data, dict):
        print("Attention : regret_T2 n'est pas un dictionnaire, utilisation d'un dictionnaire vide.")
        regret_T2_data = {}

    # Création d'une nouvelle instance de StrategyManager
    strategy_manager = StrategyManager()
    strategy_manager.regret_T1 = defaultdict(lambda: np.zeros(num_actions), regret_T1_data)
    strategy_manager.regret_T2 = defaultdict(lambda: np.zeros(num_actions), regret_T2_data)
    strategy_manager.nbr_reg = [strategy_manager.regret_T1, strategy_manager.regret_T2]

    print(f"Strategy loaded from {filepath}")
    
    
    return strategy_manager


    # Créer une nouvelle instance de StrategyManager et injecter les données
    strategy_manager = StrategyManager()
    strategy_manager.regret_T1 = defaultdict(lambda: np.zeros(num_actions), regret_T1_data)
    strategy_manager.regret_T2 = defaultdict(lambda: np.zeros(num_actions), regret_T2_data)

    print(f"[load_strategy] Strategy loaded from {filepath}")
    #print("[load_strategy] DEBUG - Loaded regret_T1:", dict(strategy_manager.regret_T1))
    #print("[load_strategy] DEBUG - Loaded regret_T2:", dict(strategy_manager.regret_T2))
    
    return strategy_manager



def load_former_strategy(filename) :
    directory = "fichier_strat"
    filepath = os.path.join(directory, filename)

    if not os.path.exists(filepath):
        print(f"No strategy file found at {filepath}")
        return None

    with open(filepath, "rb") as f:
        (M1,M2,M3,M4) = pickle.load(f)
        strategy_manager = StrategyManager()
        strategy_manager.regret_T1 = defaultdict(lambda: np.zeros(nombreActions), M3)
        strategy_manager.regret_T2 = defaultdict(lambda: np.zeros(nombreActions), M4)
        print(f"Strategy loaded from {filepath}")
        return strategy_manager


