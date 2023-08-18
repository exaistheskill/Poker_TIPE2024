from poker_variables import *
from Poker_cmplx_fct_jeu import *
from Poker_fonction_entrainement import *
import numpy as np
import os
import pickle as pck
###TEST
path = os.getcwd()
#cette partie définie des fonctions qui seront utilisés pour tester notre algo contre différentes stratégie
def tester_algo_iteration(i, nb_strat_1_T1, nb_strat_1_T2, nb_rgt_1_T1, nb_rgt_1_T2, nb_strat_2_T1, nb_strat_2_T2, nb_rgt_2_T1, nb_rgt_2_T2) :
    c = 0
    b = 0
    nombre_regret_T1 = nb_rgt_1_T1
    nombre_regret_T2 = nb_rgt_1_T2
    nombreStrategies_T1 = nb_strat_1_T1
    nombreStrategies_T2 = nb_strat_1_T2
    en_nombre_regret_T1 = nb_rgt_2_T1
    en_nombre_regret_T2 = nb_rgt_2_T2
    en_nombreStrategies_T1 = nb_strat_2_T1
    en_nombreStrategies_T2 = nb_strat_2_T2
    for k in range(i) :
        #attribution des jetons
        jeton_P1 = regle["jeton_base"]
        jeton_P2 = regle["jeton_base"]
        if k % 100000 == 0 :
            print(k)
        j = 0
        while jeton_P1 > 0 and jeton_P2 > 0 :
            #mise en place du jeu
            jeu = cree_jeu()
            P1 = jeu[0]
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
           
            
            mon_action_T1, en_action_T1 = prendre_decision_jeu_T1(j,PP1,nombre_regret_T1, nombreStrategies_T1, PP2, en_nombre_regret_T1, en_nombreStrategies_T1, jeton_P1, jeton_P2)
            
            mon_action_T1,en_action_T1, is_fold_P1, is_fold_P2, partie_continue =jouer_partie_T1(j,P1, mon_action_T1, nombreStrategies_T1, P2, en_action_T1, en_nombreStrategies_T1, jeton_P1, jeton_P2)
            
            #le Tour 1 est fini
            
            jeton_encr_P1 -= mon_action_T1
            jeton_encr_P2 -= en_action_T1
            ma_combi = combinaison_jeu(P1, flop)
            en_combi = combinaison_jeu(P2, flop)
            #on passe au Tour 2
            if partie_continue == True :
                
                mon_action_T2, en_action_T2 = prendre_decision_jeu_T2(j,PP1, ma_combi, nombreStrategies_T2, nombre_regret_T2, PP2,en_combi, en_nombreStrategies_T2, en_nombre_regret_T2, jeton_encr_P1, jeton_encr_P2)
                recomp_P1, recomp_P2 = jouer_partie_T2(j,P1,ma_combi, mon_action_T2, mon_action_T1, nombreStrategies_T2, P2,en_combi, en_action_T2, en_action_T1, en_nombreStrategies_T2 ,flop, jeton_encr_P1, jeton_encr_P2)
                
                
            else :
                if is_fold_P1 == True :
                    mon_action_T2 = -1
                    en_action_T2 = -1
                    recomp_P1 = -mon_action_T1
                    recomp_P2 = mon_action_T1
                else :
                    mon_action_T2 = -1
                    en_action_T2 = -1
                    recomp_P1 = en_action_T1
                    recomp_P2 = -en_action_T1
            ma_recomp = recomp_P1
            en_recomp = recomp_P2

            #on distribue le résultat
            jeton_P1 += recomp_P1
            jeton_P2 += recomp_P2
            j += 1
            #on les notes
        if jeton_P1 <= 0 :
            b += 1
        if jeton_P2 <= 0 :
            c += 1
    print(b,c)

def ecrire_strat_fichier_ancien(strat_T1, strat_T2, reg_T1, reg_T2, nom_fichier) :
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

def ecrire_strat_fichier(strat_T1, strat_T2, reg_T1, reg_T2, nom_fichier) :
    try :
        os.mkdir(f"{path}/strat_fichier")
    except :
        print("ok")
    F = open(f"{path}/strat_fichier/{nom_fichier}", "wb")
    pck.dump((strat_T1,strat_T2,reg_T1,reg_T2),F)
    F.close()
    
def prendre_strat_de_fichier(fichier) :
    (M1,M2,M3,M4) = pck.load(open(f"{path}/strat_fichier/{fichier}", "rb"))
    return (M1,M2,M3,M4)
def prendre_strat_de_fichier_ancien(fichier) :
    F = open(f"{path}/strat_fichier/{fichier}", "r")
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


