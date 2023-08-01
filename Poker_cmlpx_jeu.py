from poker_variables import *
from Poker_cmplx_fct_jeu import *
from Poker_test_algo import *
from numpy.random import choice as chv

def commencer_jeu(fichier_strat) :
    jeton_P1 = regle["jeton_base"]
    jeton_P2 = regle["jeton_base"]
    
    while jeton_P1 > 0 and jeton_P2 > 0 :
        #mise en place du jeu
        jeu = cree_jeu()
        P1 = jeu[0]
        PP1= conv_carte_str(P1)
        P2 = jeu[1]
        PP2 = conv_carte_str(P2)
        flop = jeu[2]
        en_nombreStrategies_T1, en_nombreStrategies_T2, en_nombre_regret_T1, en_nombre_regret_T2 = prendre_strat_de_fichier(fichier_strat)
        partie_continue = True
        is_fold_P1 = False
        tapis_P1 = False
        is_fold_P2 = False
        tapis_P2 = False
        print("votre main est : " + str(P1[0]) + str(P1[1]))
        mon_action_T1 = int(input("Quelle est votre décision ? (entrez un numéro entre 0 et 4 qui correspond à la valeur de votre bet)(nb : fold <=> 0) : "))
        if mon_action_T1 == 0 :
            is_fold_P1 = True
            partie_continue = False
            mon_action_T1 = 1
        if mon_action_T1 > jeton_P1 :
            mon_action_T1 = jeton_P1
            print("erreur fonds insuffisants, vous faites donc tapis")
            tapis_P1 = True
        en_strategie_T1 = prendre_strategie(en_nombre_regret_T1[PP2])
        en_action_T1 = prendre_decision(en_strategie_T1)
        if en_action_T1 == 0 :
            is_fold_P2 = True
            partie_continue = False
            en_action_T1 = 1
        elif en_action_T1 > jeton_P2 :
            en_action_T1 = jeton_P2
            tapis_P2 = True
        if en_action_T1 > mon_action_T1 and tapis_P1 == False and partie_continue == True:
            B = 0
            while B == 0 :
                Y = int(input(f"votre adversaire a misé {en_action_T1} , voulez vous call ? (0 : non, 1 : oui)"))
                if Y == 0 :
                    is_fold_P1 = True
                    partie_continue = False
                    B = 1
                elif Y == 1 :
                    B = 1
                    if en_action_T1 > jeton_P1 :
                        en_action_T1 = jeton_P1
                        mon_action_T1 = jeton_P1
                        tapis_P1 = True
                    else :
                        mon_action_T1 = en_action_T1
                else :
                    print("invalide, réessayez")
        elif en_action_T1 < mon_action_T1 and tapis_P2 == False and partie_continue == True :
            choix1 = prendre_strategie_moyenne(en_nombre_regret_T1[PP2])[en_action_T1]
            choix2 = 0
            a = min(mon_action_T1, jeton_P2)
            for i in range(a, len(betPossible)) :
                choix2 += prendre_strategie_moyenne(en_nombre_regret_T1[PP2])[i]
            if mon_action_T1 > jeton_P2 :
                
                mon_action_T1 = jeton_P2
                tapis_P2 = True
            choix_call = chv([0, 1], p = [choix1/(choix1 + choix2), choix2/(choix1 + choix2)])
            if choix_call == 0 :
                is_fold_P2 = True
                partie_continue = False
            elif choix_call == 1 :
                en_action_T1 = mon_action_T1
        #le Tour 1 est fini
        if is_fold_P1 == True :
            partie_continue = False
            jeton_P1 -= mon_action_T1
            jeton_P2 += mon_action_T1
            print("vous avez gagné/perdu : " + str(-1*(mon_action_T1)))
            print("votre adversaire avait : " + str(P2[0]) + str(P2[1]))
            print("il vous reste : " + str(jeton_P1))
        elif is_fold_P2 == True:
            partie_continue = False
            jeton_P1 += en_action_T1
            jeton_P2 -= en_action_T1
            print("vous avez gagné/perdu : " + str(en_action_T1))
            print("votre adversaire avait : " + str(P2[0]) + str(P2[1]))
            print("il vous reste : " + str(jeton_P1))
        else :
            print("le flop est : " + str(flop[0]) + str(flop[1]) + str(flop[2]))
            jeton_P1 -= mon_action_T1
            jeton_P2 -= en_action_T1
            en_combi = combinaison_jeu(P2, flop)
            if tapis_P1 == True or tapis_P2 == True :
                ma_recomp = prendre_recompense(mon_action_T1, P1, en_action_T1, P2, flop)
                print("vous avez gagné/perdu : " + str(ma_recomp))
                print("votre adversaire avait : " + str(P2[0]) + str(P2[1]))
                jeton_P1 += ma_recomp + mon_action_T1
                jeton_P2 -= ma_recomp + en_action_T1
                print("il vous reste : " + str(jeton_P1))
            else :
                #on passe au Tour 2
                mon_action_T2 = int(input("Quelle est votre décision ? (entrez un numéro entre 0 et 4 qui correspond à la valeur de votre bet) : "))
                if mon_action_T2 > jeton_P1 :
                    mon_action_T2 = jeton_P1
                    print("erreur fonds insuffisants, vous faites donc tapis")
                    tapis_P1 = True
                en_strategie_T2 = prendre_strategie(en_nombre_regret_T2[(PP2, en_combi[0])])
                en_action_T2 = prendre_decision(en_strategie_T2)
                if en_action_T2 > jeton_P2 :
                    en_action_T2 = jeton_P2
                    tapis_P2 = True
                if en_action_T2 > mon_action_T2 :
                    if tapis_P1 == True :
                        en_action_T2 = mon_action_T2
                    else :
                        A = 0
                        while A == 0 :
                            X = int(input(f"votre adversaire a misé {en_action_T2} , voulez vous call ? (0 : non, 1 : oui) : "))
                            if X == 0 :
                                is_fold_P1 = True
                                partie_continue = False
                                A = 1
                            elif X == 1 :
                                A = 1
                                if en_action_T2 > jeton_P1 :
                                    en_action_T2 = jeton_P1
                                    mon_action_T2 = jeton_P1
                                    tapis_P1 = True
                                else :
                                    mon_action_T2 = en_action_T2
                            else :
                                print("invalide, réessayez")
                elif en_action_T2 < mon_action_T2 :
                    if tapis_P2 == True :
                        print("votre adversaire a fait tapis, donc vous n'avez miser que : " + str(en_action_T2))
                        mon_action_T2 = en_action_T2
                    else :
                        choix1 = prendre_strategie_moyenne(en_nombre_regret_T2[(PP2, en_combi[0])])[en_action_T2]
                        choix2 = 0
                        a = min(mon_action_T1, jeton_P2)
                        for action in range(a, len(betPossible)) :
                            choix2 += prendre_strategie_moyenne(en_nombre_regret_T2[(PP2, en_combi[0])])[action]
                        if mon_action_T2 > jeton_P2 :
                            mon_action_T2= jeton_P2
                            tapis_P2 = True
                        choix_call = chv([0, 1], p = [choix1/(choix1 + choix2), choix2/(choix1 + choix2)])
                        if choix_call == 0 :
                            is_fold_P2 = True
                            partie_continue = False
                        if choix_call == 1 :
                            en_action_T2 = mon_action_T2
                if is_fold_P1 == True :
                    jeton_P1 -= mon_action_T2
                    jeton_P2 += mon_action_T2 + en_action_T1 + mon_action_T1
                    print("vous avez gagné/perdu : " + str(-1*(mon_action_T1) - mon_action_T2))
                    print("votre adversaire avait : " + str(P2[0]) + str(P2[1]))
                    print("il vous reste : " + str(jeton_P1))
                elif is_fold_P2 == True :
                    jeton_P1 += en_action_T2 + mon_action_T1 + en_action_T1
                    jeton_P2 -= en_action_T2
                    print("vous avez gagné/perdu : " + str(en_action_T2 + en_action_T1))
                    print("votre adversaire avait : " + str(P2[0]) + str(P2[1]))
                    print("il vous reste : " + str(jeton_P1))
                else :
                    ma_recomp = prendre_recompense(mon_action_T2 , P1, en_action_T2, P2, flop)
                    if ma_recomp > 0 :
                        jeton_P1 += mon_action_T1 + en_action_T1 + en_action_T2
                        jeton_P2 -= en_action_T2
                        print("vous avez gagné/perdu : " + str(en_action_T2 + en_action_T1))
                        print("votre adversaire avait : " + str(P2[0]) + str(P2[1]))
                        print("il vous reste : " + str(jeton_P1))
                    elif ma_recomp == 0 :
                        jeton_P1 += mon_action_T1
                        jeton_P2 += en_action_T1
                        print("vous avez gagné/perdu : " + str(0))
                        print("votre adversaire avait : " + str(P2[0]) + str(P2[1]))
                        print("il vous reste : " + str(jeton_P1))
                    else :
                        jeton_P1 -= mon_action_T2
                        jeton_P2 += mon_action_T2 + mon_action_T1 + en_action_T1
                        print("vous avez gagné/perdu : " + str(-1*(mon_action_T1) - mon_action_T2))
                        print("votre adversaire avait : " + str(P2[0]) + str(P2[1]))
                        print("il vous reste : " + str(jeton_P1))