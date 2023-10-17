import numpy as np
from random import choice
from numpy.random import choice as chv
from poker_variables import *
#Fonction renvoyant un couple ("combinaison", "hauteur de la combinaison","est elle en main ou pas","hauteur totale")
#Exemple : ("pair", 3,"true") veut dire qu'il y a une pair de Q (car le poids de Q est 3), de plus elle est en main, et la plus haute carte est A
def combinaison_jeu(main, flop) :
    jeu = main + flop
    ##on crée une liste de couple ("carte", occurences de la carte)
    Carte = [[j, 0,0] for j in carte_possible]
    ##on compte le nombre de carte qu'on a pour chaque symbole
    for i in range(len(jeu)) :
        for j in range(len(Carte)) :
            if Deck_symb[jeu[i]] == Carte[j][0] and i<= 2:
                Carte[j][1] += 1
            if Deck_symb[jeu[i]] == Carte[j][0] and i > 2:
                Carte[j][2] += 1
            
    ##quinte flush et carre :
    x = 0
    couleur = jeu[0][1]
    for i in range(5) :
        if (Carte[i][1] == 1 or Carte[i][2] == 1) and  jeu[i][1] == couleur :
            x += 1
        else :
            break
    if x == 5 :
        return ("quinte_flush", 1,5,True)
    ##carre et full
    x = 0
    y = 0
    for i in Carte :
        if i[1] + i[2] == 4 :
            return ("carre", 1,5,True)
    is_in_hand = False
    for i in Carte :
        if i[1] + i[2] == 3  :
            y += poids_carte[i[0]]
            is_in_hand = (i[1] != 0)
        if i[1] + i[2] == 2 :
            x += poids_carte[i[0]]
            is_in_hand = (i[1] != 0) 
        if x != 0 and y != 0:
            return ("full", y,x,True)
    if y != 0 :
        return ("brelan", y,y, is_in_hand)
    ##Flush
    x = 0
    ##a est la hauteur de notre flush
    a = 0
    for i in range(5) :
        if jeu[i][1] == couleur :
            x += 1
        else : 
            break
        if (Carte[i][1] != 0 or Carte[i][2] != 0 ) and poids_carte[Carte[i][0]] > a :
            a = poids_carte[Carte[i][0]]
    if x == 5 :
        return ("flush", a,a-1,True)
    ##suite
    x = 0
    for i in Carte :
        if (i[1] == 1 or i[2] == 1) :
            x += 1
        else :
            break
    if x == 5 :
        return ("suite", 1,1,True)
    ##double pair et pair
    x = 0
    a = 0
    b = 0
    is_in_hand = False
    for i in range(len(Carte)) :
        if (Carte[i][1] + Carte[i][2] == 2) :
            x += 1
            if a == 0 :
                a = poids_carte[Carte[i][0]]
            if a != 0 :
                b = poids_carte[Carte[i][0]]
            is_in_hand = (Carte[i][1] == 2)
    if x == 2 :
        return ("double_pair", max(a,b),min(a,b),True)
    if x == 1 :
        c = 0
        for i in range(len(Carte)) :
            if (Carte[i][1] + Carte[i][2] == 1) :
                c = max(c,poids_carte[Carte[i][0]])
        return("pair", a, c,is_in_hand)
    #hauteur
    a = 0
    for i in Carte :
        if i[1] == 1 :
            a = max(a, poids_carte[i[0]])
    return("hauteur", a,a, True)
def combinaison_jeu_ancien(main, flop) :
    jeu = main + flop
    ##on crée une liste de couple ("carte", occurences de la carte)
    Carte = [[j, 0] for j in carte_possible]
    ##on compte le nombre de carte qu'on a pour chaque symbole
    for i in range(len(jeu)) :
        for j in range(len(Carte)) :
            if Deck_symb[jeu[i]] == Carte[j][0]:
                Carte[j][1] += 1
    ##quinte flush et carre :
    x = 0
    couleur = jeu[0][1]
    for i in range(5) :
        if Carte[i][1] == 1 and  jeu[i][1] == couleur :
            x += 1
        else :
            break
    if x == 5 :
        return ("quinte_flush", 0)
    ##carre et full
    x = 0
    y = 0
    for i in Carte :
        if i[1] == 4 :
            return ("carre", 0)
    for i in Carte :
        if i[1] == 3 :
            y += poids_carte[i[0]]
        if i[1] == 2 :
            x += poids_carte[i[0]]
        if x != 0 and y != 0:
            return ("full", y)
    if y != 0 :
        return ("brelan", y)
    ##Flush
    x = 0
    ##a est la hauteur de notre flush
    a = 0
    for i in range(5) :
        if jeu[i][1] == couleur :
            x += 1
        else : 
            break
        if Carte[i][1] != 0 and poids_carte[Carte[i][0]] > a :
            a = poids_carte[Carte[i][0]]
    if x == 5 :
        return ("flush", a)
    ##suite
    x = 0
    for i in Carte :
        if i[1] == 1 :
            x += 1
        else :
            break
    if x == 5 :
        return ("suite", 0)
    ##double pair et pair
    x = 0
    a = 0
    b = 0
    for i in range(len(Carte)) :
        if Carte[i][1] == 2 :
            x += 1
            a = max(a, poids_carte[Carte[i][0]])
            b += poids_carte[Carte[i][0]]
    if x == 2 :
        return ("double_pair", max(a,b))
    if x == 1 :
        return("pair", a)
    #hauteur
    a = 0
    for i in Carte :
        if i[1] == 1 :
            a = max(a, poids_carte[i[0]])
    return("hauteur", a)
#Fonction renvoyant le poids d'une main
#Exemple : poids_main(["D2","A1"]) renvoie 6
def poids_main(main) :
    return poids_carte[Deck_symb[main[0]]] + poids_carte[Deck_symb[main[1]]]
#Fonction renvoyant le poids du flop
def poids_flop(flop) :
    return sum([poids_carte[Deck_symb[flop[i]]] for i in range(len(flop))])
#Fonction pour mettre en place un jeu de A -> Z
#Elle revoie le triplet (cartedujoueur1, cartedujoueur2, flop)
def cree_jeu() :
    P1 = []
    Carte_dis = {}
    #on prends 2 carte au hazard
    for i in range(2) :
        a= choice(choice(Deck))
        #boucle pour vérifier que la carte n'a pas encore été distribuée
        while a in Carte_dis :
            a = choice(choice(Deck))
        P1.append(a)
        Carte_dis[a] = 0
    P2 = []
    flop = []
    for i in range(2) :
        b = choice(choice(Deck))
        while b in Carte_dis :
            b = choice(choice(Deck))
        P2.append(b)
        Carte_dis[b] = 0
    for i in range(3) :
        c = choice(choice(Deck))
        while c in Carte_dis :
            c = choice(choice(Deck))
        flop.append(c)
        Carte_dis[c] = 0
    return (P1, P2, flop)
#fonction très importante qui est une bijection de [carte1, carte2] -> "carte1carte2"
def conv_carte_str(main1 : list) -> str :
    main = [Deck_symb[main1[0]], Deck_symb[main1[1]]]
    if poids_carte[main[0]] > poids_carte[main[1]] :
        return main[1] + main[0]
    else :
        return main[0] + main[1]
    
#fonction qui donne tout le temps les même carte au joueur 2
def cree_jeu_truque(carte_de_en : list) -> tuple :
    P1 = []
    Carte_dis = {carte_de_en[0] : 0, carte_de_en[1] : 0}
    #on prends 2 carte au hazard
    for i in range(2) :
        a= choice(choice(Deck))
        #boucle pour vérifier que la carte n'a pas encore été distribuée
        while a in Carte_dis :
            a = choice(choice(Deck))
        P1.append(a)
        Carte_dis[a] = 0
    P2 = carte_de_en
    flop = []
    for i in range(3) :
        c = choice(choice(Deck))
        while c in Carte_dis :
            c = choice(choice(Deck))
        flop.append(c)
        Carte_dis[c] = 0
    return (P1, P2, flop)
    
##on commence l'algo :
#fonction appliquant le CFR+ : 
def prendre_strategie_new (nombreRegrets) :
    #on prends le max en valeur absolu
    is_negatif = False
    max_abs = nombreRegrets[0]
    for i in nombreRegrets :
        if abs(i) > max_abs :
            max_abs = abs(i)
        if i < 0 :
            is_negatif = True
    #on supprime les valeur de regret négatives (car CFR+)
    strategie = np.copy(nombreRegrets)
    if is_negatif :
        for i in range(len(strategie)) :
            strategie[i] += max_abs
    #on somme les differents regrets
    sommeRegret = sum(strategie)
    if sommeRegret != 0 :
            strategie =  strategie / sommeRegret
    else :
        strategie = np.repeat(1/nombreActions, nombreActions)
    return strategie

def prendre_strategie (nombreRegrets) :
    #on supprime les valeur de regret négatives (car CFR+)
    strategie = np.clip(nombreRegrets, a_min = 0, a_max = None)
    #on somme les differents regrets
    sommeRegret = sum(strategie)
    if sommeRegret != 0 :
            strategie =  strategie / sommeRegret
    else :
        strategie = np.repeat(1/nombreActions, nombreActions)
    return strategie
    
#fonction pour afficher les résultats
def prendre_strategie_moyenne (nombreStrategies) :
    strategieMoyenne = np.zeros(nombreActions)
    sommeStrategie = sum(nombreStrategies)
    for a in range(nombreActions) :
        if sommeStrategie > 0 :
            strategieMoyenne[a] = nombreStrategies[a] / sommeStrategie
        else : 
            strategieMoyenne[a] = 1/nombreActions
    return strategieMoyenne
#fonction pour prendre les décisions à chaque coup
def prendre_decision (strategie) :
    return chv(betPossible, p = strategie)
    
    
#Fonction pour prendre la récompense
#Elle renvoie le gain ou la perte résultante de la partie
def prendre_recompense(mon_action, ma_main, en_action, en_main, flop) :
    P1 = ma_main
    P2 = en_main
    combi_P1 = combinaison_jeu(P1, flop)
    combi_P2 = combinaison_jeu(P2, flop)
    if combinaison[combi_P1[0]] > combinaison[combi_P2[0]]:
        return mon_action
    elif combinaison[combi_P1[0]] < combinaison[combi_P2[0]]:
        return -mon_action
    else :
           if combi_P1[1] > combi_P2[1] :
               return mon_action
           elif combi_P1[1] < combi_P2[1] :
               return -mon_action
           else :
               if combi_P1[2] > combi_P2[2] :
                   return mon_action
               elif combi_P1[2] < combi_P2[2] :
                   return -mon_action
               else :
                   return 0


