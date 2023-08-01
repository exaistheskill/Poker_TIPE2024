from poker_variables import *
from Poker_cmplx_fct_jeu import *
import numpy as np
from numpy.random import choice as chv

#création des dico de type regret/combi :
#ces dico sont de la forme {"DD" : [0.1, 0.1 , ..., 0.1] } (pour le T1) et {("DD", "pair") : [0.1, ..., 0.1]} (pour le T2)
nombre_regret_T1 = {}
nombre_regret_T2 = {}
for i in combi_main :
    nombre_regret_T1[conv_carte_str(i)] = np.zeros(nombreActions)
for i in combi_main_plus :
    nombre_regret_T2[(conv_carte_str(i[0]), i[1])] = np.zeros(nombreActions)
###Très important pour comprendre la suite : le "en" signifie ennemi
###En effet on "crée" virtuellement 2 joueurs qui s'affronte, donc décide d'avoir un algo et son alter ego 
en_nombre_regret_T1 = {}
en_nombre_regret_T2 = {}
for i in combi_main :
    en_nombre_regret_T1[conv_carte_str(i)] = np.zeros(nombreActions)
for i in combi_main_plus :
    en_nombre_regret_T2[(conv_carte_str(i[0]), i[1])] = np.zeros(nombreActions)
    
#dico servant à stocker la stratégie au fur et à mesure
nombreStrategies_T1 = {}
nombreStrategies_T2 = {}
for i in combi_main :
    nombreStrategies_T1[conv_carte_str(i)] = np.zeros(nombreActions)
for i in combi_main_plus :
    nombreStrategies_T2[(conv_carte_str(i[0]), i[1])] = np.zeros(nombreActions)
en_nombreStrategies_T1 = {}
en_nombreStrategies_T2= {}
for i in combi_main :
    en_nombreStrategies_T1[conv_carte_str(i)] = np.zeros(nombreActions)
for i in combi_main_plus :
    en_nombreStrategies_T2[(conv_carte_str(i[0]), i[1])] = np.zeros(nombreActions)

#fonction pour homogénisé les bets 
#càd soit les deux sont égaux soit il y a eu un fold et la fonction le renvoie
#cette fonction renvoie le 5-uplet : (monaction, l'action de mon adversaire, est ce que j'ai fold ?, est ce que il a fold ?, la partie continue t'elle ?)

def equilibrage_main_T1_print(mon_action, mon_nombre_strategie, en_action, en_nombrestrategie, ma_main, en_main, mes_jetons, en_jetons) :
    #variable pour savoir si il y a eu un fold ou pas
    is_fold_P1 = False
    is_fold_P2 = False
    #cette variable sert à gerer la cas du fold pour le 2ème tour
    partie_continue = True
    #1er cas : j'ai miser moin que l'adversaire
    if mon_action < en_action :
        #j'ai donc 2 choix : soit je fold, soit je call (mise autant que lui)
        choix1 = prendre_strategie_moyenne(mon_nombre_strategie[ma_main])[mon_action]
        #il est important de noter que je prends bien la probabilité que j'ai de "rester" sur mon choix
        #que je compte comme étant un fold(être têtu => fold)
        choix2 = 0
        a = min(en_action, mes_jetons)
        print(f"je dois raise {a} ou fold") 
        for action in range(a, len(betPossible)) :
            choix2 += prendre_strategie_moyenne(mon_nombre_strategie[ma_main])[action]
        #0 -> fold, 1 -> call
        choix_call = chv([0 , 1], p = [choix1/(choix1 + choix2), choix2/(choix1 + choix2)])
        if choix_call == 0 :
            print("j'ai fold")
            partie_continue = False
            is_fold_P1 = True
            #on donne une mise obligatoire de 1 pour éviter les abus
            mon_action = max(1, mon_action)
        elif choix_call == 1:
            print("j'ai call")
            #j'ai donc call
            mon_action, en_action =  a,a 
    #2eme cas : j'ai misé plus que mon adversaire
    elif mon_action > en_action :
        #la même que pour le 1er cas mais dans l'autre sens
        choix1 = prendre_strategie_moyenne(en_nombrestrategie[en_main])[en_action]
        choix2 = 0
        a = min(mon_action, en_jetons)
        print(f"il doit raise {a} ou fold") 
        for action in range(a, len(betPossible)) :
            choix2 += prendre_strategie_moyenne(en_nombrestrategie[en_main])[action]
        choix_call = chv([0 , 1], p = [choix1/(choix1 + choix2), choix2/(choix1 + choix2)])
        if choix_call == 0 :
            print("il fold")
            partie_continue = False
            is_fold_P2 = True
            en_action = max(1, en_action)
        elif choix_call == 1  :
            print("il call")
            en_action , mon_action = a, a
    else :
        is_fold_P1 = False
        is_fold_P2 = False
    return (mon_action, en_action, is_fold_P1, is_fold_P2, partie_continue)

def equilibrage_main_T1(mon_action, mon_nombre_strategie, en_action, en_nombrestrategie, ma_main, en_main, mes_jetons, en_jetons) :
    #variable pour savoir si il y a eu un fold ou pas
    is_fold_P1 = False
    is_fold_P2 = False
    #cette variable sert à gerer la cas du fold pour le 2ème tour
    partie_continue = True
    #1er cas : j'ai miser moin que l'adversaire
    if mon_action < en_action :
        #j'ai donc 2 choix : soit je fold, soit je call (mise autant que lui)
        choix1 = prendre_strategie_moyenne(mon_nombre_strategie[ma_main])[mon_action]
        #il est important de noter que je prends bien la probabilité que j'ai de "rester" sur mon choix
        #que je compte comme étant un fold(être têtu => fold)
        choix2 = 0
        a = min(en_action, mes_jetons)
        
        for action in range(a, len(betPossible)) :
            choix2 += prendre_strategie_moyenne(mon_nombre_strategie[ma_main])[action]
        #0 -> fold, 1 -> call
        choix_call = chv([0 , 1], p = [choix1/(choix1 + choix2), choix2/(choix1 + choix2)])
        if choix_call == 0 :
            
            partie_continue = False
            is_fold_P1 = True
            #on donne une mise obligatoire de 1 pour éviter les abus
            mon_action = max(1, mon_action)
        elif choix_call == 1:
            
            #j'ai donc call
            mon_action, en_action =  a,a 
    #2eme cas : j'ai misé plus que mon adversaire
    elif mon_action > en_action :
        #la même que pour le 1er cas mais dans l'autre sens
        choix1 = prendre_strategie_moyenne(en_nombrestrategie[en_main])[en_action]
        choix2 = 0
        a = min(mon_action, en_jetons)
        
        for action in range(a, len(betPossible)) :
            choix2 += prendre_strategie_moyenne(en_nombrestrategie[en_main])[action]
        choix_call = chv([0 , 1], p = [choix1/(choix1 + choix2), choix2/(choix1 + choix2)])
        if choix_call == 0 :
            
            partie_continue = False
            is_fold_P2 = True
            en_action = max(1, en_action)
        elif choix_call == 1  :
            
            en_action , mon_action = a, a
    else :
        is_fold_P1 = False
        is_fold_P2 = False
    return (mon_action, en_action, is_fold_P1, is_fold_P2, partie_continue)
#on crée une autre fonction adapté au T2 (notamment pour les dico) fonctionnant sur le même principe
def equilibrage_main_T2_print(mon_action,mon_nombre_strategie, en_action,en_nombrestrategie, ma_main, ma_combi, en_main, en_combi, mes_jetons, en_jetons) :
    is_fold_P1 = False
    is_fold_P2 = False
    partie_continue = True
    if mon_action < en_action :
        choix1 = prendre_strategie_moyenne(mon_nombre_strategie[(ma_main, ma_combi[0])])[mon_action]
        choix2 = 0
        a = min(en_action, mes_jetons)
        print(f"je dois raise {a} ou fold") 
        for action in range(a, len(betPossible)) :
            choix2 = prendre_strategie_moyenne(mon_nombre_strategie[(ma_main, ma_combi[0])])[action]
        choix_call = chv([0 , 1], p = [choix1/(choix1 + choix2), choix2/(choix1 + choix2)])
        if choix_call == 0 :
            print("j'ai fold")
            partie_continue = False
            is_fold_P1 = True 
            mon_action = 1
        elif choix_call == 1:
            print("j'ai call")
            mon_action, en_action = a, a
    elif mon_action > en_action :
        
        choix1 = prendre_strategie_moyenne(en_nombrestrategie[(en_main, en_combi[0])])[en_action]
        choix2 = 0
        a = min(mon_action, en_jetons)
        print(f"il doit raise {a} ou fold") 
        for action in range(a, len(betPossible)) :
            choix2 += prendre_strategie_moyenne(en_nombrestrategie[(en_main, en_combi[0])])[action]
        choix_call = chv([0 , 1], p = [choix1/(choix1 + choix2), choix2/(choix1 + choix2)])
        if choix_call == 0 :
            print("il fold")
            partie_continue = False
            is_fold_P2 = True
            en_action = 1
        elif choix_call == 1:
            print("il call")
            en_action, mon_action = a,a
    else :
        is_fold_P1 = False
        is_fold_P2 = False
        partie_continue = True
    return (mon_action, en_action, is_fold_P1, is_fold_P2, partie_continue)

def equilibrage_main_T2(mon_action,mon_nombre_strategie, en_action,en_nombrestrategie, ma_main, ma_combi, en_main, en_combi, mes_jetons, en_jetons) :
    is_fold_P1 = False
    is_fold_P2 = False
    partie_continue = True
    if mon_action < en_action :
        choix1 = prendre_strategie_moyenne(mon_nombre_strategie[(ma_main, ma_combi[0])])[mon_action]
        choix2 = 0
        a = min(en_action, mes_jetons)
        
        for action in range(a, len(betPossible)) :
            choix2 = prendre_strategie_moyenne(mon_nombre_strategie[(ma_main, ma_combi[0])])[action]
        choix_call = chv([0 , 1], p = [choix1/(choix1 + choix2), choix2/(choix1 + choix2)])
        if choix_call == 0 :
            
            partie_continue = False
            is_fold_P1 = True 
            mon_action = 1
        elif choix_call == 1:
            
            mon_action, en_action = a, a
    elif mon_action > en_action :
        
        choix1 = prendre_strategie_moyenne(en_nombrestrategie[(en_main, en_combi[0])])[en_action]
        choix2 = 0
        a = min(mon_action, en_jetons)
        
        for action in range(a, len(betPossible)) :
            choix2 += prendre_strategie_moyenne(en_nombrestrategie[(en_main, en_combi[0])])[action]
        choix_call = chv([0 , 1], p = [choix1/(choix1 + choix2), choix2/(choix1 + choix2)])
        if choix_call == 0 :
            
            partie_continue = False
            is_fold_P2 = True
            en_action = 1
        elif choix_call == 1:
            
            en_action, mon_action = a,a
    else :
        is_fold_P1 = False
        is_fold_P2 = False
        partie_continue = True
    return (mon_action, en_action, is_fold_P1, is_fold_P2, partie_continue)


#fonction pour jouer une partie de A -> Z
#cette fonction renvoie le 5-uplet : (monaction, l'action de mon adversaire, est ce que j'ai fold ?, est ce que il a fold ?, la partie continue t'elle ?)
def jouer_partie_T1_print(j,ma_main_brut, ma_decision_T1, mon_nombre_strat, en_main_brut, en_decision_T1, en_nombre_strat,mes_jeton, en_jeton) :
    PP1 = conv_carte_str(ma_main_brut)
    PP2 = conv_carte_str(en_main_brut)
    jeton_P1 = mes_jeton
    jeton_P2 = en_jeton
    #on joue le partie
    mon_action_T1 = ma_decision_T1
    en_action_T1 = en_decision_T1
    partie_continue = True
    if mon_action_T1 == 0 and j%2 == 0 :
        print("pas ce soir moi")
        mon_action_T1 = 1
    if en_action_T1 == 0 and j%2 == 1:
        print("hihi pas ce soir")
        en_action_T1 = 1
    if mon_action_T1 == 0 :
        partie_continue = False
        is_fold_P1 = True
        is_fold_P2 = False
        print("je fold")
        return (0, en_action_T1, is_fold_P1, is_fold_P2, partie_continue)
    if en_action_T1 == 0 :
        partie_continue = False
        is_fold_P1 = False
        is_fold_P2 = True
        print("il fold")
        return (mon_action_T1, 0, is_fold_P1, is_fold_P2, partie_continue)
    
    T1 = equilibrage_main_T1_print(mon_action_T1,mon_nombre_strat, en_action_T1, en_nombre_strat,PP1, PP2 ,jeton_P1, jeton_P2)
    mon_action_T1, en_action_T1, is_fold_P1, is_fold_P2, partie_continue = T1
    print(f"mon action T1 est : {mon_action_T1}")
    print(f"son action T1 est : {en_action_T1}")
    return (mon_action_T1, en_action_T1, is_fold_P1, is_fold_P2, partie_continue)

def jouer_partie_T1(j,ma_main_brut, ma_decision_T1, mon_nombre_strat, en_main_brut, en_decision_T1, en_nombre_strat,mes_jeton, en_jeton) :
    PP1 = conv_carte_str(ma_main_brut)
    PP2 = conv_carte_str(en_main_brut)
    jeton_P1 = mes_jeton
    jeton_P2 = en_jeton
    #on joue le partie
    mon_action_T1 = ma_decision_T1
    en_action_T1 = en_decision_T1
    partie_continue = True
    if mon_action_T1 == 0 and j%2 == 0 :
        
        mon_action_T1 = 1
    if en_action_T1 == 0 and j%2 == 1:
        
        en_action_T1 = 1
    if mon_action_T1 == 0 :
        partie_continue = False
        is_fold_P1 = True
        is_fold_P2 = False
        
        return (0, en_action_T1, is_fold_P1, is_fold_P2, partie_continue)
    if en_action_T1 == 0 :
        partie_continue = False
        is_fold_P1 = False
        is_fold_P2 = True
        
        return (mon_action_T1, 0, is_fold_P1, is_fold_P2, partie_continue)
    T1 = equilibrage_main_T1(mon_action_T1,mon_nombre_strat, en_action_T1, en_nombre_strat,PP1, PP2 ,jeton_P1, jeton_P2)
    mon_action_T1, en_action_T1, is_fold_P1, is_fold_P2, partie_continue = T1
    
    return (mon_action_T1, en_action_T1, is_fold_P1, is_fold_P2, partie_continue)

#cette fonction en revanche renvoie directement le résultat sous forme d'un couple (ma recompense, la recompense de mon adversaire)
def jouer_partie_T2_print(ma_main_brut ,ma_combi,ma_decision_T2,mon_action_T1, mon_nombre_strat, en_main_brut ,en_combi,en_decision_T2,en_action_T1, en_nombre_strat,flop, mes_jeton, en_jeton) :
        PP1 = conv_carte_str(ma_main_brut)
        PP2 = conv_carte_str(en_main_brut)
        jeton_P1 = mes_jeton
        jeton_P2 = en_jeton
        #on joue le partie
        mon_action_T2 = ma_decision_T2
        en_action_T2 = en_decision_T2
        
        T2 = equilibrage_main_T2_print(ma_decision_T2,mon_nombre_strat, en_action_T2, en_nombre_strat, PP1, ma_combi, PP2, en_combi ,jeton_P1, jeton_P2)
        mon_action_T2, en_action_T2, is_fold_P1, is_fold_P2, partie_continue = T2
        print(f"mon action T2 est : {mon_action_T2}")
        print(f"son action T2 est : {en_action_T2}")
        mon_action = mon_action_T1 + mon_action_T2
        en_action = en_action_T2 + en_action_T1
        #il est important de savoir si il y a eu un fold ou pas
        if is_fold_P1 == False and is_fold_P2 == False :

            ma_recomp = prendre_recompense(mon_action_T2 + mon_action_T1, ma_main_brut, en_action_T2 + en_action_T1,en_main_brut, flop)
            en_recomp = -ma_recomp
        elif is_fold_P1 == True :
            ma_recomp = -mon_action
            en_recomp = mon_action
        elif is_fold_P2 == True :
            ma_recomp = en_action
            en_recomp = -en_action
        return(ma_recomp, en_recomp)
    
def jouer_partie_T2(ma_main_brut ,ma_combi,ma_decision_T2,mon_action_T1, mon_nombre_strat, en_main_brut ,en_combi,en_decision_T2,en_action_T1, en_nombre_strat,flop, mes_jeton, en_jeton) :
        PP1 = conv_carte_str(ma_main_brut)
        PP2 = conv_carte_str(en_main_brut)
        jeton_P1 = mes_jeton
        jeton_P2 = en_jeton
        #on joue le partie
        mon_action_T2 = ma_decision_T2
        en_action_T2 = en_decision_T2
        
        T2 = equilibrage_main_T2(ma_decision_T2,mon_nombre_strat, en_action_T2, en_nombre_strat, PP1, ma_combi, PP2, en_combi ,jeton_P1, jeton_P2)
        mon_action_T2, en_action_T2, is_fold_P1, is_fold_P2, partie_continue = T2
        mon_action = mon_action_T1 + mon_action_T2
        en_action = en_action_T2 + en_action_T1
        #il est important de savoir si il y a eu un fold ou pas
        if is_fold_P1 == False and is_fold_P2 == False :

            ma_recomp = prendre_recompense(mon_action_T2 + mon_action_T1, ma_main_brut, en_action_T2 + en_action_T1,en_main_brut, flop)
            en_recomp = -ma_recomp
        elif is_fold_P1 == True :
            ma_recomp = -mon_action
            en_recomp = mon_action
        elif is_fold_P2 == True :
            ma_recomp = en_action
            en_recomp = -en_action
        return(ma_recomp, en_recomp)
#Fonction pour savoir quelle décision à été prise initialement (avant l'équilibrage)
def prendre_decision_jeu_T1_print(ma_main, mon_nombre_reg, mon_nombre_strat, en_main, en_nombre_reg,en_nombre_strat, jeton_P1, jeton_P2) :
    PP1 = ma_main
    PP2 = en_main
    ma_strategie_T1 = prendre_strategie(mon_nombre_reg[PP1])
    en_strategie_T1 = prendre_strategie(en_nombre_reg[PP2])
    for j in range(nombreActions) :
        mon_nombre_strat[PP1][j] += ma_strategie_T1[j]
        en_nombre_strat[PP2][j] += en_strategie_T1[j]
    #on joue le partie
    mon_action_T1 = prendre_decision(ma_strategie_T1)
    #contrairement aux banques moderne, ici on ne peut jouer plus que ce que l'on posséde...
    #plus sérieusement, si notre action est plus grande que nos jetons alors on fait tapis
    if mon_action_T1 > jeton_P1 :
        mon_action_T1 = jeton_P1
    
    en_action_T1 = prendre_decision(en_strategie_T1)
    if en_action_T1 > jeton_P2 :
        en_action_T1 = jeton_P2
    print("mon action initiale T1 : " + str(mon_action_T1))
    print("son action initiale T1 : " + str(en_action_T1))
    return (mon_action_T1, en_action_T1)

def prendre_decision_jeu_T1(ma_main, mon_nombre_reg, mon_nombre_strat, en_main, en_nombre_reg,en_nombre_strat, jeton_P1, jeton_P2) :
    PP1 = ma_main
    PP2 = en_main
    ma_strategie_T1 = prendre_strategie(mon_nombre_reg[PP1])
    en_strategie_T1 = prendre_strategie(en_nombre_reg[PP2])
    for j in range(nombreActions) :
        mon_nombre_strat[PP1][j] += ma_strategie_T1[j]
        en_nombre_strat[PP2][j] += en_strategie_T1[j]
    #on joue le partie
    mon_action_T1 = prendre_decision(ma_strategie_T1)
    #contrairement aux banques moderne, ici on ne peut jouer plus que ce que l'on posséde...
    #plus sérieusement, si notre action est plus grande que nos jetons alors on fait tapis
    if mon_action_T1 > jeton_P1 :
        mon_action_T1 = jeton_P1
    
    en_action_T1 = prendre_decision(en_strategie_T1)
    if en_action_T1 > jeton_P2 :
        en_action_T1 = jeton_P2
    return (mon_action_T1, en_action_T1)

def prendre_decision_jeu_T2_print(ma_main, ma_combi,mon_nombre_strat,mon_nombre_reg, en_main,en_combi, en_nombre_strat,en_nombre_reg, jeton_P1, jeton_P2) :
    PP1 = conv_carte_str(ma_main)
    PP2 = conv_carte_str(en_main)
    ma_strategie_T2 = prendre_strategie(mon_nombre_reg[(PP1, ma_combi[0])])
    en_strategie_T2 = prendre_strategie(en_nombre_reg[(PP2, en_combi[0])])
    for j in range(nombreActions) :
        mon_nombre_strat[(PP1, ma_combi[0])][j] += ma_strategie_T2[j]
        en_nombre_strat[(PP2, en_combi[0])][j] += en_strategie_T2[j]
    #on joue le partie
    mon_action_T2 = prendre_decision(ma_strategie_T2)
    if mon_action_T2 > jeton_P1 :
        mon_action_T2 = jeton_P1
    en_action_T2 = prendre_decision(en_strategie_T2)
    if en_action_T2 > jeton_P2 :
        en_action_T2 = jeton_P2
    print("mon action initiale T2 : " + str(mon_action_T2))
    print("son action initiale T2 : " + str(en_action_T2))
    return (mon_action_T2, en_action_T2)

def prendre_decision_jeu_T2(ma_main, ma_combi,mon_nombre_strat,mon_nombre_reg, en_main,en_combi,en_nombre_strat,en_nombre_reg, jeton_P1, jeton_P2) :
    PP1 = conv_carte_str(ma_main)
    PP2 = conv_carte_str(en_main)
    ma_strategie_T2 = prendre_strategie(mon_nombre_reg[(PP1, ma_combi[0])])
    en_strategie_T2 = prendre_strategie(en_nombre_reg[(PP2, en_combi[0])])
    for j in range(nombreActions) :
        mon_nombre_strat[(PP1, ma_combi[0])][j] += ma_strategie_T2[j]
        en_nombre_strat[(PP2, en_combi[0])][j] += en_strategie_T2[j]
    #on joue le partie
    mon_action_T2 = prendre_decision(ma_strategie_T2)
    if mon_action_T2 > jeton_P1 :
        mon_action_T2 = jeton_P1
    en_action_T2 = prendre_decision(en_strategie_T2)
    if en_action_T2 > jeton_P2 :
        en_action_T2 = jeton_P2
    return (mon_action_T2, en_action_T2)

def jouer_pour_regret_T1(mon_autre_coup, recomp_P1, ma_main_brut ,ma_combi, mon_nombre_strat_T1, mon_nombre_strat_T2, mon_nombre_reg_T1, mon_nombre_reg_T2, en_main_brut ,en_combi,en_action_T1, en_nombre_strat_T1, en_nombre_strat_T2 ,en_nombre_reg_T1,en_nombre_reg_T2, flop, mes_jeton, en_jeton) :
    a, P1, jeton_P1 = mon_autre_coup, ma_main_brut, mes_jeton
    P2, jeton_P2 = en_main_brut, en_jeton
    regret_act1_P1, regret_act1_P2, is_fold_P1_rgtT1, is_fold_P2_rgtT1, partie_continue_rgtT1 = jouer_partie_T1(P1, a,mon_nombre_strat_T1, P2, en_action_T1,en_nombre_strat_T1,jeton_P1, jeton_P2)
    
    jeton_rgt_P1 = jeton_P1 - regret_act1_P1
    jeton_rgt_P2 = jeton_P2 - regret_act1_P2
    if partie_continue_rgtT1 == True :
        
        regret_act2_P1, regret_act2_P2 = prendre_decision_jeu_T2(P1,ma_combi,mon_nombre_strat_T2, mon_nombre_reg_T2, P2,en_combi,en_nombre_strat_T2, en_nombre_reg_T2, jeton_rgt_P1, jeton_rgt_P2)
        mon_regret_T1 = jouer_partie_T2(P1, ma_combi,regret_act2_P1, regret_act1_P1, mon_nombre_strat_T2, P2,en_combi, regret_act2_P2, regret_act1_P2, en_nombre_strat_T2, flop, jeton_rgt_P1, jeton_rgt_P2)[0] - recomp_P1
        ma_recomp = recomp_P1
    else :
        if is_fold_P1_rgtT1 == True :
            
            mon_regret_T1 = -regret_act1_P1 - ma_recomp
            
        else :
            
            mon_regret_T1 = regret_act1_P2 - ma_recomp
    return mon_regret_T1