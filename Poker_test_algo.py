from poker_variables import *
from Poker_cmplx_fct_jeu import *
import numpy as np
import os
###TEST
path = os.getcwd()
#cette partie définie des fonctions qui seront utilisés pour tester notre algo contre différentes stratégie
def tester_algo_iteration(i, nb_strat_1_T1, nb_strat_1_T2, nb_rgt_1_T1, nb_rgt_1_T2, nb_strat_2_T1, nb_strat_2_T2, nb_rgt_2_T1, nb_rgt_2_T2) :
    L = []
    P = []
    c = 0
    b = 0
    for j in range(i) :
        #attribution des jetons
        jeton_P1 = regle["jeton_base"]
        jeton_P2 = regle["jeton_base"]
        if j%10000 == 0 :
            print(j)
        while jeton_P1 > 0 and jeton_P2 > 0 :
            #mise en place du jeu
            jeu = cree_jeu()
            P1 = jeu[1]
            # print("les cartes de l'algo sont : " + P1[0] + P1[1])
            PP1= conv_carte_str(P1)
            P2 = jeu[1]
            PP2 = conv_carte_str(P2)
            flop = jeu[2]
            #cette variable sert à ne pas écarser les jetons initiaux, étant donné 
            #qu'ils seront réutilisés dans le calcul des regrets
            jeton_encr_P1 = jeton_P1
            jeton_encr_P2 = jeton_P2
            is_fold_P1 = False
            is_fold_P2 = False
            mon_action_T1, en_action_T1 = prendre_decision_jeu_T1(PP1,nb_rgt_1_T1, nb_strat_1_T1, PP2, nb_rgt_2_T1, nb_strat_2_T1, jeton_P1, jeton_P2)
            # print("sa décision initial T1 est : " + str(mon_action_T1))
            mon_action_T1,en_action_T1, is_fold_P1, is_fold_P2, partie_continue =jouer_partie_T1(P1, mon_action_T1, nb_strat_1_T1, P2, en_action_T1, nb_strat_2_T1,flop, jeton_P1, jeton_P2)
            # print("sa décision finale T1 est : " + str(mon_action_T1))
            #le Tour 1 est fini
            
            jeton_encr_P1 -= mon_action_T1
            jeton_encr_P2 -= en_action_T1
            ma_combi = combinaison_jeu(P1, flop)
            en_combi = combinaison_jeu(P2, flop)
            #on passe au Tour 2
            if partie_continue == True :
                
                # print("le flop est : " + flop[0] + flop[1] + flop[2])
                mon_action_T2, en_action_T2 = prendre_decision_jeu_T2(PP1, ma_combi, nb_strat_1_T2, nb_rgt_1_T2, PP2,en_combi, nb_strat_2_T2, nb_rgt_2_T2, jeton_encr_P1, jeton_encr_P2)
                # print("son action T2 est : " + str(mon_action_T2))
                recomp_P1, recomp_P2 = jouer_partie_T2(P1,ma_combi, mon_action_T2, mon_action_T1, nb_strat_1_T2, P2,en_combi, en_action_T2, en_action_T1, nb_strat_2_T2 ,flop, jeton_encr_P1, jeton_encr_P2)
                # print("la récompense est : " + str(recomp_P1))
                
            else :
                #il y a eu un fold au T1
                if is_fold_P1 == True :
                    
                    # print("l'algo a fold")
                    recomp_P1 = -mon_action_T1
                    recomp_P2 = mon_action_T1
                    # print("la récompense est : " + str(recomp_P1))
                else :
                    
                    # print("l'adversaire a fold")
                    recomp_P1 = en_action_T1
                    recomp_P2 = -en_action_T1
                    # print("la récompense est : " + str(recomp_P1))
            
            ma_recomp = recomp_P1
            en_recomp = recomp_P2
            #on prends le regret
            for a in range(nombreActions) :
                #regret du TOUR1 :
                #a représente une autre branche de l'arbre des actions, càd une autre action
                #on ne regarde que les regrets possible (pas au dessus de nos moyens)
                if a <= jeton_P1 :
                    #on joue la partie
                    regret_act1_P1, regret_act1_P2, is_fold_P1_rgtT1, is_fold_P2_rgtT1, partie_continue_rgtT1 = jouer_partie_T1(P1, a,nb_strat_1_T1, P2, en_action_T1,nb_strat_2_T1, flop, jeton_P1, jeton_P2)
                    
                    jeton_rgt_P1 = jeton_P1 - regret_act1_P1
                    jeton_rgt_P2 = jeton_P2 - regret_act1_P2
                    if partie_continue_rgtT1 == True :
                        regret_act2_P1, regret_act2_P2 = prendre_decision_jeu_T2(P1,ma_combi,nb_strat_1_T2, nb_rgt_1_T2, P2,en_combi,nb_strat_2_T2,nb_rgt_2_T2, jeton_rgt_P1, jeton_rgt_P2)
                        mon_regret_T1 = jouer_partie_T2(P1, ma_combi,regret_act2_P1, regret_act1_P1, nb_strat_1_T2, P2,en_combi, regret_act2_P2, regret_act1_P2, nb_strat_2_T2, flop, jeton_rgt_P1, jeton_rgt_P2)[0] - recomp_P1
                        
                    else :
                        if is_fold_P1_rgtT1 == True :
                            
                            mon_regret_T1 = -regret_act1_P1 - ma_recomp
                            
                        else :
                            
                            mon_regret_T1 = regret_act1_P2 - ma_recomp
                            
                    nb_rgt_1_T1[PP1][a] += mon_regret_T1
                #on passe au regret de l'alter ego de notre algo
                if a <= jeton_P2 :
                    regret_act1_P2, regret_act1_P1, is_fold_P2_rgtT1, is_fold_P1_rgtT1, partie_continue_rgtT1 = jouer_partie_T1(P2, a, nb_strat_2_T1, P1, mon_action_T1, nb_strat_1_T1, flop, jeton_P2, jeton_P1)
                    jeton_rgt_P1 = jeton_P1 - regret_act1_P1
                    jeton_rgt_P2 = jeton_P2 - regret_act1_P2
                    if partie_continue_rgtT1 == True :
                        regret_act2_P1, regret_act2_P2 = prendre_decision_jeu_T2(P1, ma_combi, nb_strat_1_T2, nb_rgt_1_T2, P2, en_combi,nb_strat_2_T2, nb_rgt_2_T2, jeton_rgt_P1, jeton_rgt_P2)
                        en_regret_T1 = jouer_partie_T2(P1,ma_combi, regret_act2_P1, regret_act1_P1, nb_strat_1_T2, P2,en_combi, regret_act2_P2, regret_act1_P2,nb_strat_2_T2, flop, jeton_rgt_P1, jeton_rgt_P2)[1] - recomp_P2
                    else :
                        if is_fold_P1_rgtT1 == True :
                            en_regret_T1 = regret_act1_P1 - en_recomp
                        else :
                            en_regret_T1 = -regret_act1_P2 - en_recomp
                    nb_rgt_2_T1[PP2][a] += en_regret_T1
                #regret du TOUR2
                
                if is_fold_P1 == False and is_fold_P2 == False :
                    if a <= jeton_P1 - mon_action_T1 :
                        regret_T2_P1 = jouer_partie_T2(P1, ma_combi,a, mon_action_T1, nb_strat_1_T2, P2,en_combi, en_action_T2, en_action_T1, nb_strat_2_T2, flop, jeton_P1 - mon_action_T1, jeton_P2 - en_action_T1)[0] - ma_recomp
                        nombre_regret_T2[(PP1, ma_combi[0])][a] += regret_T2_P1
                    if a <= jeton_P2 - en_action_T1 :
                        regret_T2_P2 = jouer_partie_T2(P2,en_combi, a, en_action_T1, nb_strat_2_T2, P1, ma_combi, mon_action_T2, mon_action_T1, nb_strat_1_T2,flop, jeton_P2 - en_action_T1, jeton_P1 - mon_action_T1)[1] - en_recomp
                        nb_rgt_2_T2[(PP2, en_combi[0])][a] += regret_T2_P2
            #on distribue le résultat
            
            jeton_P1 += recomp_P1 
            jeton_P2 += recomp_P2
            #on les notes
            b += recomp_P1
            print(b)
            c += recomp_P2
            print(c)
            L.append(c)
            P.append(b)
    return (L,P)

def ecrire_strat_fichier(strat_T1, strat_T2, reg_T1, reg_T2, nom_fichier) :
    try :
        os.mkdir(f"{path}/strat_fichier")
    except :
        print("ok")
    F = open(f"{path}/strat_fichier/{nom_fichier}", "w")
    j = 0
    for i in strat_T1 :
        if j == 0 :
            F.write(str(strat_T1[i][0]))
            for k in range(1, len(betPossible)) :
                F.write("\n" + str(strat_T1[i][k]))
        else :
            for k in range(len(betPossible)) :
                F.write("\n" + str(strat_T1[i][k]))
        j = 1
    for i in strat_T2 :
        for k in range(len(betPossible)) :
            F.write("\n" + str(strat_T2[i][j]))
    for i in reg_T1 :
        for k in range(len(betPossible)) :
            F.write("\n" + str(reg_T1[i][j]))
    for i in reg_T2 :
        for k in range(len(betPossible)) :
            F.write("\n" + str(reg_T2[i][k]))
    F.close()
    
def prendre_strat_de_fichier(fichier) :
    F = open(f"{path}/strat_fichier/fichier", "r")
    L = F.read().split("\n")
    k = 0
    dico_strat_1_T1 = {}
    for i in nombreStrategies_T1 :
        dico_strat_1_T1[i] = np.zeros(len(betPossible))
        for l in range(len(betPossible)) :
            dico_strat_1_T1[i][l] = float(L[k])
            k += 1
    dico_strat_1_T2 = {}
    for i in nombreStrategies_T2 :
        dico_strat_1_T2[i] = np.zeros(len(betPossible))
        for l in range(len(betPossible)) :
            dico_strat_1_T2[i][l] = float(L[k])
            k += 1
    dico_reg_1_T1 = {}
    for i in nombre_regret_T1 :
        dico_reg_1_T1[i] = np.zeros(len(betPossible))
        for l in range(len(betPossible)) :
            dico_reg_1_T1[i][l] = float(L[k])
            k += 1
    dico_reg_1_T2 = {}
    for i in nombre_regret_T2 :
        dico_reg_1_T2[i] = np.zeros(len(betPossible))
        for l in range(len(betPossible)) :
            dico_reg_1_T2[i][l] = float(L[k])
            k += 1
    return (dico_strat_1_T1, dico_strat_1_T2, dico_reg_1_T1, dico_reg_1_T2)

def test_amelioration_algo(iteration1, iteration2) :
    assert iteration2 >= iteration1
    entrainer(iteration1)
    F = open(f"strategy_goat{iteration1//77}.txt", "w")
    j = 0
    for i in nombreStrategies_T1 :
        if j == 0 :
            F.write(str(nombreStrategies_T1[i][0]))
            for k in range(1, len(betPossible)) :
                F.write("\n" + str(nombreStrategies_T1[i][k]))
        else :
            for k in range(len(betPossible)) :
                F.write("\n" + str(nombreStrategies_T1[i][k]))
        j = 1
    for i in nombreStrategies_T2 :
        for k in range(len(betPossible)) :
            F.write("\n" + str(nombreStrategies_T2[i][j]))
    for i in nombre_regret_T1 :
        for k in range(len(betPossible)) :
            F.write("\n" + str(nombre_regret_T1[i][j]))
    for i in nombre_regret_T2 :
        for k in range(len(betPossible)) :
            F.write("\n" + str(nombre_regret_T2[i][k]))
    F.close()
    dico_strat_1_T1, dico_strat_1_T2, dico_reg_1_T1, dico_reg_1_T2 = prendre_strat_de_fichier(f"strategy_goat{iteration1//77}.txt")
    entrainer(iteration2 - iteration1)
    Resultat = tester_algo_iteration(10000, dico_strat_1_T1, dico_strat_1_T2, dico_reg_1_T1, dico_reg_1_T2, nombreStrategies_T1, nombreStrategies_T2, nombre_regret_T1, nombre_regret_T2)
    return Resultat

def test_entre_2_strat(iterations, fichier_strat_1, fichier_strat_2) :
    dico_strat_1_T1, dico_strat_1_T2, dico_reg_1_T1, dico_reg_1_T2 = prendre_strat_de_fichier(fichier_strat_1)
    dico_strat_2_T1, dico_strat_2_T2, dico_reg_2_T1, dico_reg_2_T2 = prendre_strat_de_fichier(fichier_strat_2)
    result = tester_algo_iteration(iterations,  dico_strat_1_T1, dico_strat_1_T2, dico_reg_1_T1, dico_reg_1_T2, dico_strat_2_T1, dico_strat_2_T2, dico_reg_2_T1, dico_reg_2_T2)
    return result
