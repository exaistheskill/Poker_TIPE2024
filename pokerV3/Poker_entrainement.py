from poker_variables import *
from Poker_cmplx_fct_jeu import *
from Poker_fonction_entrainement import *
from Poker_test_algo import *
import matplotlib.pyplot as plt
from random import randint
import pickle as pck

#mise en place de l'algo
def entrainer(i) :
    W, L = 0, 0
    trucT1 = ('JK',2,2)
    trucT2 = ('JK', ('pair', 4, 5, True), 3)
    set1 = []
    set2 = []
    for k in range(i) :
        #attribution des jetons
        jeton_P1 = regle["jeton_base"]
        jeton_P2 = regle["jeton_base"]
        if k % 1000 == 0 :
            print(k)
        j = 0
        while jeton_P1 > 0 and jeton_P2 > 0 :
            #mise en place du jeu
            jeu = cree_jeu()
            P1 = jeu[1]
            PP1= conv_carte_str(P1)
            
            P2 = jeu[0]
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
            
            le_reg_1 = [[] for i in range(nombreActions) ]
            le_reg_2 = [[] for i in range(nombreActions)]
            #on prends le regret
            for a in range(nombreActions) :
                #regret du TOUR1 :
                #a représente une autre branche de l'arbre des actions, càd une autre action
                #on ne regarde que les regrets possible (pas au dessus de nos moyens)
                if a <= jeton_P1 and a != mon_action_T1 and a >= 1 - j%2:
                    #on joue la partie
                    #print("je regarde si j'avais joué au T1 : " + str(a) )
                    regret_act1_P1, regret_act1_P2, is_fold_P1_rgtT1, is_fold_P2_rgtT1, partie_continue_rgtT1 = jouer_partie_T1(j, P1, a,nombreStrategies_T1, P2, en_action_T1,en_nombreStrategies_T1, jeton_P1, jeton_P2)
                    
                    jeton_rgt_P1 = jeton_P1 - regret_act1_P1
                    jeton_rgt_P2 = jeton_P2 - regret_act1_P2
                    if partie_continue_rgtT1 == True :
                        regret_act2_P1, regret_act2_P2 = prendre_decision_jeu_T2(j,P1,ma_combi,nombreStrategies_T2, nombre_regret_T2, P2,en_combi,en_nombreStrategies_T2, en_nombre_regret_T2, jeton_rgt_P1, jeton_rgt_P2)
                        mon_regret_T1 = jouer_partie_T2(j,P1, ma_combi,regret_act2_P1, regret_act1_P1, nombreStrategies_T2, P2,en_combi, regret_act2_P2, regret_act1_P2, en_nombreStrategies_T2, flop, jeton_rgt_P1, jeton_rgt_P2)[0] - recomp_P1
                        
                    else :
                        if is_fold_P1_rgtT1 == True :
                            
                            mon_regret_T1 = -regret_act1_P1 - ma_recomp
                            
                        else :
                            
                            mon_regret_T1 = regret_act1_P2 - ma_recomp
                    
                    #print("mon regret est donc de : " + str(mon_regret_T1))
                    #le_reg_1[a].append(mon_regret_T1)
                    if j%2 == 0 :
                        nombre_regret_T1[(PP1,-1)][a] += mon_regret_T1
                    if j%2 == 1 :
                        nombre_regret_T1[(PP1,en_action_T1)][a] += mon_regret_T1
                        if (PP1,en_action_T1,a) == trucT1 :
                            set1.append(nombreStrategies_T1[(PP1,en_action_T1)])
                #on passe au regret de l'alter ego de notre algo
                if a <= jeton_P2 and a != en_action_T1 and a >= j%2 :
                    
                    regret_act1_P1, regret_act1_P2, is_fold_P1_rgtT1, is_fold_P2_rgtT1, partie_continue_rgtT1 = jouer_partie_T1(j,P1, mon_action_T1, nombreStrategies_T1,P2, a, en_nombreStrategies_T1,  jeton_P2, jeton_P1)
                    jeton_rgt_P1 = jeton_P1 - regret_act1_P1
                    jeton_rgt_P2 = jeton_P2 - regret_act1_P2
                    if partie_continue_rgtT1 == True :
                        regret_act2_P1, regret_act2_P2 = prendre_decision_jeu_T2(j,P1, ma_combi, nombreStrategies_T2, nombre_regret_T2, P2, en_combi,en_nombreStrategies_T2, en_nombre_regret_T2, jeton_rgt_P1, jeton_rgt_P2)
                        en_regret_T1 = jouer_partie_T2(j,P1,ma_combi, regret_act2_P1, regret_act1_P1, nombreStrategies_T2, P2,en_combi, regret_act2_P2, regret_act1_P2,en_nombreStrategies_T2, flop, jeton_rgt_P1, jeton_rgt_P2)[1] - recomp_P2
                    else :
                        if is_fold_P1_rgtT1 == True :
                            en_regret_T1 = regret_act1_P1 - en_recomp
                        else :
                            en_regret_T1 = -regret_act1_P2 - en_recomp
                    
                   
                    if j%2 == 0 :
                        en_nombre_regret_T1[(PP2,mon_action_T1)][a] += en_regret_T1
                        if (PP2,mon_action_T1,a) == trucT1 :
                            set2.append(en_nombreStrategies_T1[(PP2,mon_action_T1)])
                    if j%2 == 1 :
                        en_nombre_regret_T1[(PP2,-1)][a] += en_regret_T1
                        
                    le_reg_1[a].append(en_regret_T1)
                    
                #regret du TOUR2
                
                if is_fold_P1 == False and is_fold_P2 == False :
                    if a <= jeton_P1 - mon_action_T1 and a != mon_action_T2 and a >= j%2:
                        #print("je regarde si j'avais joué au T2 : " + str(a))
                        regret_T2_P1 = jouer_partie_T2(j,P1, ma_combi,a, mon_action_T1, nombreStrategies_T2, P2,en_combi, en_action_T2, en_action_T1, en_nombreStrategies_T2, flop, jeton_P1 - mon_action_T1, jeton_P2 - en_action_T1)[0] - ma_recomp
                        
                        #le_reg_2[a].append(regret_T2_P1)
                        #print("mon regret est de : " + str(regret_T2_P1))
                        if j%2 == 0 :
                            nombre_regret_T2[(PP1, ma_combi,en_action_T2)][a] += regret_T2_P1
                        if j%2 == 1 :
                            nombre_regret_T2[(PP1, ma_combi,-1)][a] += regret_T2_P1
                    if a <= jeton_P2 - en_action_T1 and a != en_action_T2 and a >= 1 - j%2:
                        
                        
                        regret_T2_P2 = jouer_partie_T2(j,P1, ma_combi,mon_action_T2 , mon_action_T1, nombreStrategies_T2, P2,en_combi, a, en_action_T1, en_nombreStrategies_T2, flop, jeton_P1 - mon_action_T1, jeton_P2 - en_action_T1)[1] - en_recomp
                        
                        if j%2 == 0 :
                            en_nombre_regret_T2[(PP2, en_combi,-1)][a] += regret_T2_P2
                        if j%2 == 1:
                            en_nombre_regret_T2[(PP2, en_combi, mon_action_T2)][a] += regret_T2_P2
                        le_reg_2[a].append(regret_T2_P2)
                       
            #on distribue le résultat
            jeton_P1 += recomp_P1
            jeton_P2 += recomp_P2
            j += 1
        if jeton_P1 <= 0 :
            L +=1
        if jeton_P2 <= 0 :
            W += 1
    print(W, L)
    return set1,set2
def entrainer_print(i) :
    W, L = 0, 0
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
            print("mes cartes : " + PP1)
            P2 = jeu[1]
            PP2 = conv_carte_str(P2)
            print("cartes adversaire : " + PP2)
            flop = jeu[2]
            print("le flop est : " + flop[0] + flop[1] + flop[2] )
            if j%2 == 0 :
                print("tour pair")
            else :
                print("tour impair")
            #cette variable sert à ne pas écarser les jetons initiaux, étant donné 
            #qu'ils seront réutilisés dans le calcul des regrets
            jeton_encr_P1 = jeton_P1
            jeton_encr_P2 = jeton_P2
            is_fold_P1 = False
            is_fold_P2 = False
            print("Debut du T1")
            
            mon_action_T1, en_action_T1 = prendre_decision_jeu_T1_print(j,PP1,nombre_regret_T1, nombreStrategies_T1, PP2, en_nombre_regret_T1, en_nombreStrategies_T1, jeton_P1, jeton_P2)
            
            mon_action_T1,en_action_T1, is_fold_P1, is_fold_P2, partie_continue =jouer_partie_T1_print(j,P1, mon_action_T1, nombreStrategies_T1, P2, en_action_T1, en_nombreStrategies_T1, jeton_P1, jeton_P2)
            
            #le Tour 1 est fini
            
            jeton_encr_P1 -= mon_action_T1
            jeton_encr_P2 -= en_action_T1
            ma_combi = combinaison_jeu(P1, flop)
            en_combi = combinaison_jeu(P2, flop)
            #on passe au Tour 2
            if partie_continue == True :
                print("Debut du T2")
                mon_action_T2, en_action_T2 = prendre_decision_jeu_T2_print(j,PP1, ma_combi, nombreStrategies_T2, nombre_regret_T2, PP2,en_combi, en_nombreStrategies_T2, en_nombre_regret_T2, jeton_encr_P1, jeton_encr_P2)
                recomp_P1, recomp_P2 = jouer_partie_T2_print(j,P1,ma_combi, mon_action_T2, mon_action_T1, nombreStrategies_T2, P2,en_combi, en_action_T2, en_action_T1, en_nombreStrategies_T2 ,flop, jeton_encr_P1, jeton_encr_P2)
                
                
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
            
            le_reg_1 = [[] for i in range(nombreActions) ]
            le_reg_2 = [[] for i in range(nombreActions)]
            #on prends le regret
            for a in range(nombreActions) :
                #regret du TOUR1 :
                #a représente une autre branche de l'arbre des actions, càd une autre action
                #on ne regarde que les regrets possible (pas au dessus de nos moyens)
                if a <= jeton_P1 and a != mon_action_T1 and a >= 1 - j%2:
                    #on joue la partie
                    #print("je regarde si j'avais joué au T1 : " + str(a) )
                    regret_act1_P1, regret_act1_P2, is_fold_P1_rgtT1, is_fold_P2_rgtT1, partie_continue_rgtT1 = jouer_partie_T1(j, P1, a,nombreStrategies_T1, P2, en_action_T1,en_nombreStrategies_T1, jeton_P1, jeton_P2)
                    
                    jeton_rgt_P1 = jeton_P1 - regret_act1_P1
                    jeton_rgt_P2 = jeton_P2 - regret_act1_P2
                    if partie_continue_rgtT1 == True :
                        regret_act2_P1, regret_act2_P2 = prendre_decision_jeu_T2(j,P1,ma_combi,nombreStrategies_T2, nombre_regret_T2, P2,en_combi,en_nombreStrategies_T2, en_nombre_regret_T2, jeton_rgt_P1, jeton_rgt_P2)
                        mon_regret_T1 = jouer_partie_T2(j,P1, ma_combi,regret_act2_P1, regret_act1_P1, nombreStrategies_T2, P2,en_combi, regret_act2_P2, regret_act1_P2, en_nombreStrategies_T2, flop, jeton_rgt_P1, jeton_rgt_P2)[0] - recomp_P1
                        
                    else :
                        if is_fold_P1_rgtT1 == True :
                            
                            mon_regret_T1 = -regret_act1_P1 - ma_recomp
                            
                        else :
                            
                            mon_regret_T1 = regret_act1_P2 - ma_recomp
                    
                    #print("mon regret est donc de : " + str(mon_regret_T1))
                    #le_reg_1[a].append(mon_regret_T1)
                    if j%2 == 0 :
                        nombre_regret_T1[(PP1,-1)][a] += mon_regret_T1
                    if j%2 == 1 :
                        nombre_regret_T1[(PP1,en_action_T1)][a] += mon_regret_T1
                #on passe au regret de l'alter ego de notre algo
                if a <= jeton_P2 and a != en_action_T1 and a >= j%2 :
                    print("mon adversaire apprends")
                    print("il regarde si il'avait joué au T1 : " + str(a) )
                    regret_act1_P1, regret_act1_P2, is_fold_P1_rgtT1, is_fold_P2_rgtT1, partie_continue_rgtT1 = jouer_partie_T1_print(j,P1, mon_action_T1, nombreStrategies_T1,P2, a, en_nombreStrategies_T1,  jeton_P2, jeton_P1)
                    jeton_rgt_P1 = jeton_P1 - regret_act1_P1
                    jeton_rgt_P2 = jeton_P2 - regret_act1_P2
                    if partie_continue_rgtT1 == True :
                        regret_act2_P1, regret_act2_P2 = prendre_decision_jeu_T2_print(j,P1, ma_combi, nombreStrategies_T2, nombre_regret_T2, P2, en_combi,en_nombreStrategies_T2, en_nombre_regret_T2, jeton_rgt_P1, jeton_rgt_P2)
                        en_regret_T1 = jouer_partie_T2_print(j,P1,ma_combi, regret_act2_P1, regret_act1_P1, nombreStrategies_T2, P2,en_combi, regret_act2_P2, regret_act1_P2,en_nombreStrategies_T2, flop, jeton_rgt_P1, jeton_rgt_P2)[1] - recomp_P2
                    else :
                        if is_fold_P1_rgtT1 == True :
                            en_regret_T1 = regret_act1_P1 - en_recomp
                        else :
                            en_regret_T1 = -regret_act1_P2 - en_recomp
                    
                   
                    if j%2 == 0 :
                        en_nombre_regret_T1[(PP2,mon_action_T1)][a] += en_regret_T1
                    if j%2 == 1 :
                        en_nombre_regret_T1[(PP2,-1)][a] += en_regret_T1
                    le_reg_1[a].append(en_regret_T1)
                    print("son regret est donc de : " + str(en_regret_T1))
                    print("c'est bon il a fini")
                #regret du TOUR2
                
                if is_fold_P1 == False and is_fold_P2 == False :
                    if a <= jeton_P1 - mon_action_T1 and a != mon_action_T2 and a >= j%2:
                        #print("je regarde si j'avais joué au T2 : " + str(a))
                        regret_T2_P1 = jouer_partie_T2(j,P1, ma_combi,a, mon_action_T1, nombreStrategies_T2, P2,en_combi, en_action_T2, en_action_T1, en_nombreStrategies_T2, flop, jeton_P1 - mon_action_T1, jeton_P2 - en_action_T1)[0] - ma_recomp
                        
                        #le_reg_2[a].append(regret_T2_P1)
                        #print("mon regret est de : " + str(regret_T2_P1))
                        if j%2 == 0 :
                            nombre_regret_T2[(PP1, ma_combi,en_action_T2)][a] += regret_T2_P1
                        if j%2 == 1 :
                            nombre_regret_T2[(PP1, ma_combi,-1)][a] += regret_T2_P1
                    if a <= jeton_P2 - en_action_T1 and a != en_action_T2 and a >= 1 - j%2:
                        print("mon adversaire apprends")
                        print("il regarde si il'avait joué au T2 : " + str(a))
                        
                        regret_T2_P2 = jouer_partie_T2_print(j,P1, ma_combi,mon_action_T2 , mon_action_T1, nombreStrategies_T2, P2,en_combi, a, en_action_T1, en_nombreStrategies_T2, flop, jeton_P1 - mon_action_T1, jeton_P2 - en_action_T1)[1] - en_recomp
                        
                        if j%2 == 0 :
                            en_nombre_regret_T2[(PP2, en_combi,-1)][a] += regret_T2_P2
                        if j%2 == 1:
                            en_nombre_regret_T2[(PP2, en_combi, mon_action_T2)][a] += regret_T2_P2
                        le_reg_2[a].append(regret_T2_P2)
                        print("son regret est de : " + str(regret_T2_P2))
                        print("il a fini")
            #on distribue le résultat
            jeton_P1 += recomp_P1
            jeton_P2 += recomp_P2
            print("mes jetons restants : " + str(jeton_P1))
            print("ses jetons restants : " + str(jeton_P2))
            print("évolution du regret : ")
            if j%2 == 0 :
                print(en_nombre_regret_T1[(PP2,mon_action_T1)])
                print(en_nombre_regret_T2[(PP2, en_combi,-1)])
                print("la stratégie est : ")
                print(prendre_strategie(en_nombre_regret_T1[(PP2,mon_action_T1)]))
                print(prendre_strategie(en_nombre_regret_T2[(PP2, en_combi,-1)]))
            if j%2 == 1 :
                print(en_nombre_regret_T1[(PP2,-1)])
                print(en_nombre_regret_T2[(PP2, en_combi,mon_action_T2)])
                print("la stratégie est : ")
                print(prendre_strategie(en_nombre_regret_T1[(PP2,-1)]))
                print(prendre_strategie(en_nombre_regret_T2[(PP2, en_combi,mon_action_T2)]))
            print("le regret de ce tour :")
            print(le_reg_1)
            print(le_reg_2)
            j += 1
        if jeton_P1 <= 0 :
            L +=1
        if jeton_P2 <= 0 :
            W += 1
    print(W, L)
    
####Terminal
# L1,L2 = entrainer(10000)
# n,m = len(L1),len(L2)
# p = max(n,m)
# k = min(n,m)
# plt.figure()
# X = np.linspace(1,k,k)
# plt.plot(X,L1[n-k:n], color='red')
# plt.plot(X,L2[m-k:m],color='blue')
# plt.show()

#S1 ,S2 = entrainer(10000)

##écrire une strat dans un fichier
iteration = 1
entrainer(iteration)
var = randint(0,iteration*100)
ecrire_strat_fichier(nombreStrategies_T1, nombreStrategies_T2, nombre_regret_T1, nombre_regret_T2, f"strat{iteration}_{var}.txt")


