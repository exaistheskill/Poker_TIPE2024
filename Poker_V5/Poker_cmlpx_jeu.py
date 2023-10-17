from poker_variables import *
from Poker_cmplx_fct_jeu import *
from Poker_test_algo import *
from numpy.random import choice as chv

def commencer_jeu(fichier_strat) :
    jeton_P1_reel = regle["jeton_base"]
    jeton_P2_reel = regle["jeton_base"]
    j = 0
    while jeton_P1_reel > 0 and jeton_P2_reel > 0 :
        #mise en place du jeu
        jeton_P1 = jeton_P1_reel
        jeton_P2 = jeton_P2_reel
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
        
        #Debut du T1
        if j%2 == 0 :
            print("vous avez une mise obligatoire de 1")
            if jeton_P1 == 1 :
                print("vous all in !")
                tapis_P1 = True
                mon_action_T1 = 1
            else : 
                mon_action_T1 = int(input("Quelle est votre décision ? (entrez un numéro entre 0 et 4 qui correspond à la valeur de votre bet) : "))
                while mon_action_T1 <= 0 or mon_action_T1 > 4 :
                    mon_action_T1 = int(input("Quelle est votre décision ? (entrez un numéro entre 0 et 4 qui correspond à la valeur de votre bet) : "))
            if mon_action_T1 == 0 :
                is_fold_P1 = True
                partie_continue = False
            if mon_action_T1 > jeton_P1 :
                mon_action_T1 = jeton_P1
                print("erreur fonds insuffisants, vous faites donc tapis")
                tapis_P1 = True
            en_strategie_T1 = prendre_strategie(en_nombre_regret_T1[(PP2,mon_action_T1)])
            en_action_T1 = prendre_decision(en_strategie_T1)
            if en_action_T1 == 0 :
                is_fold_P2 = True
                partie_continue = False
            elif en_action_T1 > jeton_P2 :
                en_action_T1 = jeton_P2
                tapis_P2 = True
            elif en_action_T1 < mon_action_T1 :
                print("l'adversaire a fold")
                en_action_T1 = 0
                is_fold_P2 = True
                partie_continue= False
            if en_action_T1 > jeton_P1 :
                en_action_T1 = jeton_P1
            if en_action_T1 > mon_action_T1 and not(is_fold_P1) :
                choix = 2
                while not choix in [0,1] :
                    choix = int(input(f"vous voulez call {en_action_T1} ou fold ? (1->call, 0 -> fold)"))
                if choix == 0 :
                    print("vous avez fold")
                    is_fold_P1 = True
                    partie_continue = False
                if choix == 1 :
                    mon_action_T1 = en_action_T1
        if j%2 == 1 :
            print("il a une mise obligatoire de 1")
            if jeton_P2 == 1 :
                print("il all in !")
                tapis_P2 = True
                en_action_T1 = 1
            else : 
                en_strategie_T1 = prendre_strategie(en_nombre_regret_T1[(PP2,-1)])
                en_action_T1 = max(prendre_decision(en_strategie_T1),1)
            if en_action_T1 >= jeton_P2 :
                en_action_T1 = jeton_P2
                tapis_P2 = True
                print("il all in")
            print(f"son action est {en_action_T1}")
            mon_action_T1 = int(input(f"Quelle est votre décision ? (entrez un numéro entre 0 et 4 qui correspond à la valeur de votre bet)(nb : fold <=> ma mise < {en_action_T1}) : "))
            if mon_action_T1 >= jeton_P1 :
                mon_action_T1 = jeton_P1
                print("vous faites donc tapis")
                tapis_P1 = True
            elif mon_action_T1 < en_action_T1 :
                is_fold_P1 = True
                partie_continue = False
                mon_action_T1 = 0
            if mon_action_T1 > en_action_T1 and not(is_fold_P2):
                if mon_action_T1 > jeton_P2 :
                    print("vous avez misé plus que les jetons de l'adversaire")
                    mon_action_T1 = jeton_P2
                if tapis_P2 :
                    mon_action_T1 = en_action_T1
                    print(f"comme il a all in donc on ne joue que {jeton_P2}")
                else :
                    tetu = 0
                    for action in range(0, mon_action_T1 -1) :
                        tetu += prendre_strategie(en_nombre_regret_T1[(PP2,mon_action_T1)])[action]
                    call = 0
                    for action in range(mon_action_T1,len(betPossible)) :
                        call += prendre_strategie(en_nombre_regret_T1[(PP2,mon_action_T1)])[action]
                    choix = chv([0,1], p = [tetu/(call + tetu), call/(call + tetu)])
                    if choix == 0 :
                        print("il fold")
                        is_fold_P2 = True
                        partie_continue = False
                    if choix == 1:
                        print("il call")
                        en_action_T1 = mon_action_T1
        if mon_action_T1 == jeton_P1 :
            tapis_P1 = True
        if en_action_T1 == jeton_P2 :
            tapis_P2 = True
        #le Tour 1 est fini
        if is_fold_P1 == True :
            partie_continue = False
            jeton_P1_reel -= mon_action_T1
            jeton_P2_reel += mon_action_T1
            print("vous avez gagné/perdu : " + str(-1*(mon_action_T1)))
            print("votre adversaire avait : " + str(P2[0]) + str(P2[1]))
            
        elif is_fold_P2 == True:
            partie_continue = False
            jeton_P1_reel += en_action_T1
            jeton_P2_reel -= en_action_T1
            print("vous avez gagné/perdu : " + str(en_action_T1))
            print("votre adversaire avait : " + str(P2[0]) + str(P2[1]))
            
        else :
            print("le flop est : " + str(flop[0]) + str(flop[1]) + str(flop[2]))
            jeton_P1 -= mon_action_T1
            jeton_P2 -= en_action_T1
            en_combi = combinaison_jeu(P2, flop)
            if tapis_P1 == True or tapis_P2 == True :
                ma_recomp = prendre_recompense(mon_action_T1, P1, en_action_T1, P2, flop)
                if ma_recomp != 0 :
                    print("vous avez gagné/perdu : " + str(ma_recomp))
                    print("votre adversaire avait : " + str(P2[0]) + str(P2[1]))
                    jeton_P1_reel += ma_recomp 
                    jeton_P2_reel -= ma_recomp
                    
                else :
                    print("vous avez gagné/perdu : " + str(ma_recomp))
                    print("votre adversaire avait : " + str(P2[0]) + str(P2[1]))
                    jeton_P1 += mon_action_T1
                    jeton_P2 += en_action_T1
                    
            else :
                #on passe au Tour 2
                if j%2 == 1 :
                    print("vous avez une mise obligatoire de 1")
                    if jeton_P1 == 1 :
                        print("vous all in !")
                        tapis_P1 = True
                        mon_action_T2 = 1
                    else : 
                        mon_action_T2 = int(input("Quelle est votre décision ? (entrez un numéro entre 0 et 4 qui correspond à la valeur de votre bet): "))
                        while mon_action_T2 <= 0 or mon_action_T2 > 4 :
                            mon_action_T1 = int(input("Quelle est votre décision ? (entrez un numéro entre 0 et 4 qui correspond à la valeur de votre bet) : "))
                    if mon_action_T2 == 0 :
                        is_fold_P1 = True
                        partie_continue = False
                    if mon_action_T2 > jeton_P1 :
                        mon_action_T2 = jeton_P1
                        print("erreur fonds insuffisants, vous faites donc tapis")
                        tapis_P1 = True
                    if mon_action_T2 == jeton_P1 :
                        tapis_P1 = True
                    en_strategie_T2 = prendre_strategie(en_nombre_regret_T2[(PP2,en_combi,mon_action_T2)])
                    en_action_T2 = prendre_decision(en_strategie_T2)
                    print("son action initiale est " + str(en_action_T2))
                    if en_action_T2 == 0 :
                        is_fold_P2 = True
                        print("il a fold")
                        partie_continue = False
                    elif en_action_T2 > jeton_P2 :
                        en_action_T2 = jeton_P2
                        tapis_P2 = True
                        print("il all in")
                    elif en_action_T2 < mon_action_T2 :
                        print("il a fold")
                        en_action_T2 = 0
                        is_fold_P2 = True
                        partie_continue= False
                    if en_action_T2 > jeton_P1 :
                        en_action_T2 = jeton_P1
                    if en_action_T2 > mon_action_T2 and not(is_fold_P1) :
                        choix = 2
                        while not choix in [0,1] :
                            choix = int(input(f"vous voulez call {en_action_T2} ou fold ? (1->call, 0 -> fold)"))
                        if choix == 0 :
                            print("vous avez fold")
                            mon_action_T2 = 1
                            is_fold_P1 = True
                            partie_continue = False
                        if choix == 1 :
                            mon_action_T2 = en_action_T2
                if j%2 == 0 :
                    print("il a une mise obligatoire de 1")
                    if jeton_P2 == 1 :
                        print("il all in !")
                        tapis_P2 = True
                        en_action_T2 = 1
                    else : 
                        en_strategie_T2 = prendre_strategie(en_nombre_regret_T2[(PP2,en_combi,-1)])
                        en_action_T2 = max(prendre_decision(en_strategie_T2),1)
                    if en_action_T2 >= jeton_P2 :
                        en_action_T2 = jeton_P2
                        tapis_P2 = True
                        print("il all in")
                    print(f"son action est {en_action_T2}")
                    mon_action_T2 = int(input(f"Quelle est votre décision ? (entrez un numéro entre 0 et 4 qui correspond à la valeur de votre bet)(nb : fold <=> ma mise < {en_action_T2}) : "))
                    if mon_action_T2 >= jeton_P1 :
                        mon_action_T2 = jeton_P1
                        print("vous faites donc tapis")
                        tapis_P1 = True
                    elif mon_action_T2 < en_action_T2 :
                        is_fold_P1 = True
                        partie_continue = False
                        mon_action_T2 = 0
                    if mon_action_T2 > en_action_T2 and not(is_fold_P2):
                        if mon_action_T2 > jeton_P2 :
                            print("vous avez misé plus que les jetons de l'adversaire")
                            mon_action_T2 = jeton_P2
                        if tapis_P2 :
                            mon_action_T2 = en_action_T2
                            print(f"comme il a all in donc on ne joue que {jeton_P2}")
                        else :
                            tetu = 0
                            for action in range(0, mon_action_T2 -1) :
                                tetu += prendre_strategie(en_nombre_regret_T2[(PP2,en_combi ,mon_action_T2)])[action]
                            call = 0
                            for action in range(mon_action_T2,len(betPossible)) :
                                call += prendre_strategie(en_nombre_regret_T2[(PP2, en_combi ,mon_action_T2)])[action]
                            choix = chv([0,1], p = [tetu/(call + tetu), call/(call + tetu)])
                            if choix == 0 :
                                print("il fold")
                                is_fold_P2 = True
                                partie_continue = False
                            if choix == 1:
                                print("il call")
                                en_action_T2 = mon_action_T2
                if is_fold_P1 == True :
                    jeton_P1_reel -= mon_action_T2 + mon_action_T1
                    jeton_P2_reel += mon_action_T2 + mon_action_T1
                    print("vous avez gagné/perdu : " + str(-1*(mon_action_T1) - mon_action_T2))
                    print("votre adversaire avait : " + str(P2[0]) + str(P2[1]))
                    
                elif is_fold_P2 == True :
                    jeton_P1_reel += en_action_T2 + en_action_T1
                    jeton_P2_reel -= en_action_T2 + en_action_T1
                    print("vous avez gagné/perdu : " + str(en_action_T2 + en_action_T1))
                    print("votre adversaire avait : " + str(P2[0]) + str(P2[1]))
                    
                else :
                    ma_recomp = prendre_recompense(mon_action_T2, P1, en_action_T2, P2, flop)
                    if ma_recomp != 0 :
                        a = ma_recomp + mon_action_T1*(abs(ma_recomp)//ma_recomp)
                        print("vous avez gagné/perdu : " + str(a))
                        print("votre adversaire avait : " + str(P2[0]) + str(P2[1]))
                        jeton_P1_reel += a
                        jeton_P2_reel -= ma_recomp + en_action_T1*(abs(ma_recomp)//ma_recomp)
                        
                    else :
                        print("vous avez gagné/perdu : " + str(ma_recomp))
                        print("votre adversaire avait : " + str(P2[0]) + str(P2[1]))
                        jeton_P1 += mon_action_T1
                        jeton_P2 += en_action_T1
                        
        print("vos jetons : " + str(jeton_P1_reel))
        print("les jetons de l'adversaire : " + str(jeton_P2_reel))
        j += 1