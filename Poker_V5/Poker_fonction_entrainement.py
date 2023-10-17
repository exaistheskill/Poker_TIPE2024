from poker_variables import *
from Poker_cmplx_fct_jeu import *
import numpy as np
from numpy.random import choice as chv

#création des dico de type regret/combi :
#ces dico sont de la forme {("DD",2) : [0.1, 0.1 , ..., 0.1] } (pour le T1, où "DD" est un exemple de main et 2 est le coup de l'adversaire)
#par défaut si on commence on considère le coup de l'adversaire comme étant égal à -1
# et {("DD", "pair") : [0.1, ..., 0.1]} (pour le T2)
###Très important pour comprendre la suite : le "en" signifie ennemi
###En effet on "crée" virtuellement 2 joueurs qui s'affronte, donc décide d'avoir un algo et son alter ego 
nombre_regret_T1 = {}
nombre_regret_T2 = {}
en_nombre_regret_T1 = {}
en_nombre_regret_T2 = {}
nombreStrategies_T1 = {}
nombreStrategies_T2 = {}
en_nombreStrategies_T1 = {}
en_nombreStrategies_T2= {}
for i in combi_main :
    for j in range(-1,nombreActions) :
        for k in combinaison :
            for l in range(1,len(carte_possible)+1) :
                for n in range(1,len(carte_possible)+1) :
                    for m in [False, True] :
                        nombre_regret_T2[(conv_carte_str(i), (k,l,n,m),j)] = np.zeros(nombreActions) 
                        en_nombre_regret_T2[(conv_carte_str(i), (k,l,n,m),j)] = np.zeros(nombreActions) 
                        nombreStrategies_T2[(conv_carte_str(i), (k,l,n,m),j)] = np.zeros(nombreActions) 
                        en_nombreStrategies_T2[(conv_carte_str(i), (k,l,n,m),j)] = np.zeros(nombreActions) 
for i in combi_main :
    for j in range(-1,nombreActions) :
        en_nombre_regret_T1[(conv_carte_str(i),j)] = np.zeros(nombreActions) 
        nombre_regret_T1[(conv_carte_str(i),j)] = np.zeros(nombreActions) 
        nombreStrategies_T1[(conv_carte_str(i),j)] = np.zeros(nombreActions) 
        en_nombreStrategies_T1[(conv_carte_str(i),j)] = np.zeros(nombreActions)



#dico servant à stocker la stratégie au fur et à mesure

       

#fonction pour homogénisé les bets 
#càd soit les deux sont égaux soit il y a eu un fold et la fonction le renvoie
#cette fonction renvoie le 5-uplet : (monaction, l'action de mon adversaire, est ce que j'ai fold ?, est ce que il a fold ?, la partie continue t'elle ?)



def equilibrage_main_T1_new(j,mon_action, mon_nombre_strategie, en_action, en_nombrestrategie, ma_main, en_main, mes_jetons, en_jetons) :
    #variable pour savoir si il y a eu un fold ou pas
    is_fold_P1 = False
    is_fold_P2 = False
    
    partie_continue = True
    #1er cas : je commence !
    if j%2 == 0 :
        
        #1.1eme cas : j'ai misé plus que mon adversaire
        if mon_action > en_action :
            if en_action == en_jetons :
                mon_action = en_jetons
                return (mon_action, en_action, is_fold_P1, is_fold_P2, partie_continue)
            #l'adversaire a donc fold
            is_fold_P2 = True
            partie_continue = False
            return (mon_action, 0, is_fold_P1, is_fold_P2, partie_continue)
        #1.2eme cas : il a raise
        if mon_action < en_action :
            #si j'avais all in donc :
            if mon_action == mes_jetons :
                en_action = mes_jetons
                return (mon_action, en_action, is_fold_P1, is_fold_P2, partie_continue)
            #j'ai donc 2 choix : soit je fold, soit je call (mise autant que lui)
            choix1 = prendre_strategie(mon_nombre_strategie[(ma_main,en_action)])[mon_action]
            for action in range(mon_action) :
                choix1 += prendre_strategie(mon_nombre_strategie[(ma_main,en_action)])[action]
            #il est important de noter que je prends bien la probabilité que j'ai de "rester" sur mon choix
            #que je compte comme étant un fold(être têtu => fold)
            choix2 = 0
            a = min(en_action, mes_jetons)
           
            for action in range(a, len(betPossible)) :
                choix2 += prendre_strategie(mon_nombre_strategie[(ma_main,en_action)])[action]
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
        else :
            is_fold_P1 = False
            is_fold_P2 = False
        return (mon_action, en_action, is_fold_P1, is_fold_P2, partie_continue)
    #2ème cas : c'est mon adversaire qui commence
    if j%2 == 1 :
        #2.1 cas : 
        if mon_action < en_action :
            if mon_action == mes_jetons :
                en_action = mes_jetons
                return (mon_action, en_action, is_fold_P1, is_fold_P2, partie_continue)
            # j'ai donc fold
            
            is_fold_P1 = True
            partie_continue = False
            return (0, en_action, is_fold_P1, is_fold_P2, partie_continue)
        
        if mon_action > en_action :
            
            #il a donc 2 choix : soit il fold, soit il call (mise autant que moi)
            choix1 = prendre_strategie(en_nombrestrategie[(en_main,mon_action)])[en_action]
            for action in range(en_action) :
                choix1 += prendre_strategie(en_nombrestrategie[(en_main,mon_action)])[action]
            #il est important de noter que je prends bien la probabilité que j'ai de "rester" sur mon choix
            #que je compte comme étant un fold(être têtu => fold)
            choix2 = 0
            a = min(mon_action, en_jetons)
            if en_action == en_jetons :
                mon_action = en_jetons
                return (mon_action, en_action, is_fold_P1, is_fold_P2, partie_continue)
            for action in range(a, len(betPossible)) :
                choix2 += prendre_strategie(en_nombrestrategie[(en_main,mon_action)])[action]
            #0 -> fold, 1 -> call
            choix_call = chv([0 , 1], p = [choix1/(choix1 + choix2), choix2/(choix1 + choix2)])
            if choix_call == 0 :
                
                partie_continue = False
                is_fold_P2 = True
                #on donne une mise obligatoire de 1 pour éviter les abus
                en_action = max(1, en_action)
            elif choix_call == 1:
               
                #j'ai donc call
                mon_action, en_action =  a,a 
        else :
            is_fold_P1 = False
            is_fold_P2 = False
        return (mon_action, en_action, is_fold_P1, is_fold_P2, partie_continue)




def equilibrage_main_T1(j,mon_action, mon_nombre_strategie, en_action, en_nombrestrategie, ma_main, en_main, mes_jetons, en_jetons) :
    #variable pour savoir si il y a eu un fold ou pas
    is_fold_P1 = False
    is_fold_P2 = False
    
    partie_continue = True
    #1er cas : je commence !
    if j%2 == 0 :
        
        #1.1eme cas : j'ai misé plus que mon adversaire
        if mon_action > en_action :
            if en_action == en_jetons :
                mon_action = en_jetons
                return (mon_action, en_action, is_fold_P1, is_fold_P2, partie_continue)
            #l'adversaire a donc fold
            is_fold_P2 = True
            partie_continue = False
            return (mon_action, 0, is_fold_P1, is_fold_P2, partie_continue)
        #1.2eme cas : il a raise
        elif mon_action < en_action :
            
            #j'ai donc 2 choix : soit je fold, soit je call (mise autant que lui)
            choix1 = prendre_strategie_moyenne(mon_nombre_strategie[(ma_main,en_action)])[mon_action]
            #il est important de noter que je prends bien la probabilité que j'ai de "rester" sur mon choix
            #que je compte comme étant un fold(être têtu => fold)
            choix2 = 0
            a = min(en_action, mes_jetons)
            if mon_action == mes_jetons :
                en_action = mes_jetons
                return (mon_action, en_action, is_fold_P1, is_fold_P2, partie_continue)
            for action in range(a, len(betPossible)) :
                choix2 += prendre_strategie_moyenne(mon_nombre_strategie[(ma_main,en_action)])[action]
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
        else :
            is_fold_P1 = False
            is_fold_P2 = False
        return (mon_action, en_action, is_fold_P1, is_fold_P2, partie_continue)
    elif j%2 == 1 :
        if en_action > mon_action :
            if mon_action == mes_jetons :
                en_action = mes_jetons
                return (mon_action, en_action, is_fold_P1, is_fold_P2, partie_continue)
            # j'ai donc fold
            
            is_fold_P1 = True
            partie_continue = False
            return (0, en_action, is_fold_P1, is_fold_P2, partie_continue)
        
        elif mon_action > en_action :
            
            #il a donc 2 choix : soit il fold, soit il call (mise autant que moi)
            choix1 = prendre_strategie_moyenne(en_nombrestrategie[(en_main,mon_action)])[en_action]
            #il est important de noter que je prends bien la probabilité que j'ai de "rester" sur mon choix
            #que je compte comme étant un fold(être têtu => fold)
            choix2 = 0
            a = min(mon_action, en_jetons)
            if en_action == en_jetons :
                mon_action = en_jetons
                return (mon_action, en_action, is_fold_P1, is_fold_P2, partie_continue)
            for action in range(a, len(betPossible)) :
                choix2 += prendre_strategie_moyenne(en_nombrestrategie[(en_main,mon_action)])[action]
            #0 -> fold, 1 -> call
            choix_call = chv([0 , 1], p = [choix1/(choix1 + choix2), choix2/(choix1 + choix2)])
            if choix_call == 0 :
                
                partie_continue = False
                is_fold_P2 = True
                #on donne une mise obligatoire de 1 pour éviter les abus
                en_action = max(1, en_action)
            elif choix_call == 1:
               
                #j'ai donc call
                mon_action, en_action =  a,a 
        else :
            is_fold_P1 = False
            is_fold_P2 = False
        return (mon_action, en_action, is_fold_P1, is_fold_P2, partie_continue)
#on crée une autre fonction adapté au T2 (notamment pour les dico) fonctionnant sur le même principe
def equilibrage_main_T2(j,mon_action,mon_nombre_strategie, en_action,en_nombrestrategie, ma_main, ma_combi, en_main, en_combi, mes_jetons, en_jetons) :
    is_fold_P1 = False
    is_fold_P2 = False
    partie_continue = True
    if j%2 == 0 :
        
        if mon_action < en_action :
            if mon_action == mes_jetons :
                
                return(mon_action, mon_action,is_fold_P1,is_fold_P2,partie_continue)
            #donc j'ai fold
            
            is_fold_P1 = True
            partie_continue = False
            return (0,en_action, is_fold_P1,is_fold_P2,partie_continue)
        elif mon_action > en_action :
            
            choix1 = prendre_strategie_moyenne(en_nombrestrategie[(en_main, en_combi,mon_action)])[en_action]
            choix2 = 0
            a = min(mon_action, en_jetons)
            if en_action == en_jetons :
                
                return (a, a, is_fold_P1, is_fold_P2, partie_continue)
           
            for action in range(a, len(betPossible)) :
                choix2 += prendre_strategie_moyenne(en_nombrestrategie[(en_main, en_combi,mon_action)])[action]
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
    if j%2 == 1 :
        if mon_action > en_action :
            if en_action == en_jetons :
                
                return(en_action,en_action,is_fold_P1,is_fold_P2,partie_continue)
            #il a donc fold
            
            is_fold_P2, partie_continue = True, False
            return(mon_action, 0, is_fold_P1,is_fold_P2, partie_continue)
        elif mon_action < en_action :
            choix1 = prendre_strategie_moyenne(mon_nombre_strategie[(ma_main, ma_combi, en_action)])[mon_action]
            choix2 = 0
            a = min(en_action, mes_jetons)
            if mon_action == mes_jetons :
                
                return (a, a, is_fold_P1, is_fold_P2, partie_continue)
           
            for action in range(a, len(betPossible)) :
                choix2 = prendre_strategie_moyenne(mon_nombre_strategie[(ma_main, ma_combi,en_action)])[action]
            choix_call = chv([0 , 1], p = [choix1/(choix1 + choix2), choix2/(choix1 + choix2)])
            if choix_call == 0 :
               
                partie_continue = False
                is_fold_P1 = True 
                mon_action = 1
            elif choix_call == 1:
                
                mon_action, en_action = a, a
       
        else :
            is_fold_P1 = False
            is_fold_P2 = False
            partie_continue = True
        return (mon_action, en_action, is_fold_P1, is_fold_P2, partie_continue)
    
    
def equilibrage_main_T2_save(j,mon_action,mon_nombre_strategie, en_action,en_nombrestrategie, ma_main, ma_combi, en_main, en_combi, mes_jetons, en_jetons) :
    is_fold_P1 = False
    is_fold_P2 = False
    partie_continue = True
    if j%2 == 0 :
        
        if mon_action < en_action :
            if mon_action == mes_jetons :
                return(mon_action, mon_action,is_fold_P1,is_fold_P2,partie_continue)
            #donc j'ai fold
            
            is_fold_P1 = True
            partie_continue = False
            return (0,en_action, is_fold_P1,is_fold_P2,partie_continue)
        elif mon_action > en_action :
            
            choix1 = prendre_strategie_moyenne(en_nombrestrategie[(en_main, en_combi,mon_action)])[en_action]
            choix2 = 0
            a = min(mon_action, en_jetons)
            if en_action == en_jetons :
                
                return (a, a, is_fold_P1, is_fold_P2, partie_continue)
           
            for action in range(a, len(betPossible)) :
                choix2 += prendre_strategie_moyenne(en_nombrestrategie[(en_main, en_combi,mon_action)])[action]
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
    if j%2 == 1 :
        if mon_action > en_action :
            if en_action == en_jetons :
                return(en_action,en_action,is_fold_P1,is_fold_P2,partie_continue)
            #il a donc fold
            
            is_fold_P2, partie_continue = False, False
            return(mon_action, 0, is_fold_P1,is_fold_P2, partie_continue)
        if mon_action < en_action :
            choix1 = prendre_strategie_moyenne(mon_nombre_strategie[(ma_main, ma_combi, en_action)])[mon_action]
            choix2 = 0
            a = min(en_action, mes_jetons)
            if mon_action == mes_jetons :
                
                return (a, a, is_fold_P1, is_fold_P2, partie_continue)
           
            for action in range(a, len(betPossible)) :
                choix2 = prendre_strategie_moyenne(mon_nombre_strategie[(ma_main, ma_combi,en_action)])[action]
            choix_call = chv([0 , 1], p = [choix1/(choix1 + choix2), choix2/(choix1 + choix2)])
            if choix_call == 0 :
               
                partie_continue = False
                is_fold_P1 = True 
                mon_action = 1
            elif choix_call == 1:
                
                mon_action, en_action = a, a
       
        else :
            is_fold_P1 = False
            is_fold_P2 = False
            partie_continue = True
        return (mon_action, en_action, is_fold_P1, is_fold_P2, partie_continue)


#fonction pour jouer une partie de A -> Z
#cette fonction renvoie le 5-uplet : (monaction, l'action de mon adversaire, est ce que j'ai fold ?, est ce que il a fold ?, la partie continue t'elle ?)


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
    T1 = equilibrage_main_T1(j,mon_action_T1,mon_nombre_strat, en_action_T1, en_nombre_strat,PP1, PP2 ,jeton_P1, jeton_P2)
    #T1 = equilibrage_main_T1(j, en_action_T1, en_nombre_strat,mon_action_T1,mon_nombre_strat, PP2 ,PP1, jeton_P2,jeton_P1)
    mon_action_T1, en_action_T1, is_fold_P1, is_fold_P2, partie_continue = T1
    #en_action_T1, mon_action_T1 ,  is_fold_P2, is_fold_P1, partie_continue = T1
    
    return (mon_action_T1, en_action_T1, is_fold_P1, is_fold_P2, partie_continue)

#cette fonction en revanche renvoie directement le résultat sous forme d'un couple (ma recompense, la recompense de mon adversaire)

def jouer_partie_T2(j,ma_main_brut ,ma_combi,ma_decision_T2,mon_action_T1, mon_nombre_strat, en_main_brut ,en_combi,en_decision_T2,en_action_T1, en_nombre_strat,flop, mes_jeton, en_jeton) :
        PP1 = conv_carte_str(ma_main_brut)
        PP2 = conv_carte_str(en_main_brut)
        jeton_P1 = mes_jeton
        jeton_P2 = en_jeton
        #on joue le partie
        mon_action_T2 = ma_decision_T2
        en_action_T2 = en_decision_T2
        
        #T2 = equilibrage_main_T2(j,ma_decision_T2,mon_nombre_strat, en_action_T2, en_nombre_strat, PP1, ma_combi, PP2, en_combi ,jeton_P1, jeton_P2)
        T2 = equilibrage_main_T2(j+1,en_decision_T2,en_nombre_strat, mon_action_T2, mon_nombre_strat, PP2, en_combi, PP1, ma_combi ,jeton_P2, jeton_P1)
        #mon_action_T2, en_action_T2, is_fold_P1, is_fold_P2, partie_continue = T2
        en_action_T2, mon_action_T2,  is_fold_P2,  is_fold_P1, partie_continue = T2
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


def prendre_decision_jeu_T1(j,ma_main, mon_nombre_reg, mon_nombre_strat, en_main, en_nombre_reg,en_nombre_strat, jeton_P1, jeton_P2) :
   PP1 = ma_main
   PP2 = en_main
   if j%2 == 0 :
       ma_strategie_T1 = prendre_strategie(mon_nombre_reg[(PP1,-1)])
       #contrairement aux banques moderne, ici on ne peut jouer plus que ce que l'on posséde...
       #plus sérieusement, si notre action est plus grande que nos jetons alors on fait tapis
       #De plus on a obligation de misé dans un tour pair
       mon_action_T1 = max(min(jeton_P1, prendre_decision(ma_strategie_T1)),1)
       en_strategie_T1 = prendre_strategie(en_nombre_reg[(PP2, mon_action_T1)])
       en_action_T1 = min(prendre_decision(en_strategie_T1),jeton_P2)
       for k in range(nombreActions) :
            mon_nombre_strat[(PP1,-1)][k] += ma_strategie_T1[k]
            en_nombre_strat[(PP2,mon_action_T1)][k] += en_strategie_T1[k]
   elif j%2 == 1 :
       en_strategie_T1 = prendre_strategie(en_nombre_reg[(PP2,-1)])
       en_action_T1 = max(min(jeton_P2, prendre_decision(en_strategie_T1)),1)
       ma_strategie_T1 = prendre_strategie(mon_nombre_reg[(PP1, en_action_T1)])
       mon_action_T1 = min(prendre_decision(ma_strategie_T1),jeton_P1)
       for k in range(nombreActions) :
            mon_nombre_strat[(PP1,en_action_T1)][k] += ma_strategie_T1[k]
            en_nombre_strat[(PP2,-1)][k] += en_strategie_T1[k]
  
   return (mon_action_T1, en_action_T1)


   
    

def prendre_decision_jeu_T2(j,ma_main, ma_combi,mon_nombre_strat,mon_nombre_reg, en_main,en_combi,en_nombre_strat,en_nombre_reg, jeton_P1, jeton_P2) :
    PP1 = conv_carte_str(ma_main)
    PP2 = conv_carte_str(en_main)
    if j%2 == 0 :
        en_strategie_T2 = prendre_strategie(en_nombre_reg[(PP2, en_combi,-1)])
        en_action_T2 = min(prendre_decision(en_strategie_T2),jeton_P2)
        ma_strategie_T2 = prendre_strategie(mon_nombre_reg[(PP1, ma_combi,en_action_T2)])
        mon_action_T2 = min(prendre_decision(ma_strategie_T2), jeton_P1)
        for j in range(nombreActions) :
            mon_nombre_strat[(PP1, ma_combi,en_action_T2)][j] += ma_strategie_T2[j]
            en_nombre_strat[(PP2, en_combi,-1)][j] += en_strategie_T2[j]
        
        return (mon_action_T2, en_action_T2)
    if j%2 == 1 :
        ma_strategie_T2 = prendre_strategie(mon_nombre_reg[(PP1, ma_combi,-1)])
        mon_action_T2 = min(prendre_decision(ma_strategie_T2),jeton_P1)
        en_strategie_T2 = prendre_strategie(en_nombre_reg[(PP2, en_combi,mon_action_T2)])
        en_action_T2 = min(prendre_decision(en_strategie_T2), jeton_P2)
        for j in range(nombreActions) :
            mon_nombre_strat[(PP1, ma_combi,-1)][j] += ma_strategie_T2[j]
            en_nombre_strat[(PP2, en_combi,mon_action_T2)][j] += en_strategie_T2[j]
        
        return (mon_action_T2, en_action_T2)

def jouer_pour_regret_T1(mon_autre_coup, j, recomp_P1, ma_main_brut ,ma_combi, mon_nombre_strat_T1, mon_nombre_strat_T2, mon_nombre_reg_T1, mon_nombre_reg_T2, en_main_brut ,en_combi,en_action_T1, en_nombre_strat_T1, en_nombre_strat_T2 ,en_nombre_reg_T1,en_nombre_reg_T2, flop, mes_jeton, en_jeton) :
    a, P1, jeton_P1 = mon_autre_coup, ma_main_brut, mes_jeton
    P2, jeton_P2 = en_main_brut, en_jeton
    regret_act1_P1, regret_act1_P2, is_fold_P1_rgtT1, is_fold_P2_rgtT1, partie_continue_rgtT1 = jouer_partie_T1(j, P1, a,mon_nombre_strat_T1, P2, en_action_T1,en_nombre_strat_T1,jeton_P1, jeton_P2)
    ma_recomp = recomp_P1
    jeton_rgt_P1 = jeton_P1 - regret_act1_P1
    jeton_rgt_P2 = jeton_P2 - regret_act1_P2
    if partie_continue_rgtT1 == True :
        
        regret_act2_P1, regret_act2_P2 = prendre_decision_jeu_T2(P1,ma_combi,mon_nombre_strat_T2, mon_nombre_reg_T2, P2,en_combi,en_nombre_strat_T2, en_nombre_reg_T2, jeton_rgt_P1, jeton_rgt_P2)
        mon_regret_T1 = jouer_partie_T2(P1, ma_combi,regret_act2_P1, regret_act1_P1, mon_nombre_strat_T2, P2,en_combi, regret_act2_P2, regret_act1_P2, en_nombre_strat_T2, flop, jeton_rgt_P1, jeton_rgt_P2)[0] - recomp_P1
        
    else :
        if is_fold_P1_rgtT1 == True :
            
            mon_regret_T1 = -regret_act1_P1 - ma_recomp
            
        else :
            
            mon_regret_T1 = regret_act1_P2 - ma_recomp
    return mon_regret_T1

## Version Print

def equilibrage_main_T1_print(j,mon_action, mon_nombre_strategie, en_action, en_nombrestrategie, ma_main, en_main, mes_jetons, en_jetons) :
    #variable pour savoir si il y a eu un fold ou pas
    is_fold_P1 = False
    is_fold_P2 = False
    #cette variable sert à gerer la cas du fold pour le 2ème tour
    partie_continue = True
    #1er cas : j'ai miser moin que l'adversaire
    if j%2 == 0 :
        
        #2eme cas : j'ai misé plus que mon adversaire
        if mon_action > en_action :
            if en_action == en_jetons :
                print("il all in")
                mon_action = en_jetons
                return (mon_action,en_action,is_fold_P1,is_fold_P2,partie_continue)
            print("il fold")
            #l'adversaire a donc fold
            is_fold_P2 = True
            partie_continue = False
            return (mon_action, 0, is_fold_P1, is_fold_P2, partie_continue)
        
        if mon_action < en_action :
            
            #j'ai donc 2 choix : soit je fold, soit je call (mise autant que lui)
            choix1 = prendre_strategie_moyenne(mon_nombre_strategie[(ma_main,en_action)])[mon_action]
            #il est important de noter que je prends bien la probabilité que j'ai de "rester" sur mon choix
            #que je compte comme étant un fold(être têtu => fold)
            choix2 = 0
            a = min(en_action, mes_jetons)
            if mon_action == mes_jetons :
                print("j'ai all in")
                en_action = mes_jetons
                return (mon_action, en_action, is_fold_P1, is_fold_P2, partie_continue)
            print(f"je dois raise {a} ou fold")
            for action in range(a, len(betPossible)) :
                choix2 += prendre_strategie_moyenne(mon_nombre_strategie[(ma_main,en_action)])[action]
            #0 -> fold, 1 -> call
            choix_call = chv([0 , 1], p = [choix1/(choix1 + choix2), choix2/(choix1 + choix2)])
            if choix_call == 0 :
                print("je fold")
                partie_continue = False
                is_fold_P1 = True
                #on donne une mise obligatoire de 1 pour éviter les abus
                mon_action = max(1, mon_action)
            elif choix_call == 1:
                print("je call")
                #j'ai donc call
                mon_action, en_action =  a,a 
        else :
            is_fold_P1 = False
            is_fold_P2 = False
        return (mon_action, en_action, is_fold_P1, is_fold_P2, partie_continue)
    if j%2 == 1 :
        if mon_action < en_action :
            if mon_action == mes_jetons :
                en_action = mes_jetons
                print("j'ai all in")
                return (mon_action, en_action, is_fold_P1, is_fold_P2, partie_continue)
            # j'ai donc fold
            print("je fold")
            is_fold_P1 = True
            partie_continue = False
            return (0, en_action, is_fold_P1, is_fold_P2, partie_continue)
        
        if mon_action > en_action :
            
            #il a donc 2 choix : soit il fold, soit il call (mise autant que moi)
            choix1 = prendre_strategie_moyenne(en_nombrestrategie[(en_main,mon_action)])[en_action]
            #il est important de noter que je prends bien la probabilité que j'ai de "rester" sur mon choix
            #que je compte comme étant un fold(être têtu => fold)
            choix2 = 0
            a = min(mon_action, en_jetons)
            if en_action == en_jetons :
                print("il all in")
                mon_action = en_jetons
                return (mon_action, en_action, is_fold_P1, is_fold_P2, partie_continue)
            print(f"il doit raise {a} ou fold")
            for action in range(a, len(betPossible)) :
                choix2 += prendre_strategie_moyenne(en_nombrestrategie[(en_main,mon_action)])[action]
            #0 -> fold, 1 -> call
            choix_call = chv([0 , 1], p = [choix1/(choix1 + choix2), choix2/(choix1 + choix2)])
            if choix_call == 0 :
                print("il fold")
                partie_continue = False
                is_fold_P2 = True
                #on donne une mise obligatoire de 1 pour éviter les abus
                en_action = max(1, en_action)
            elif choix_call == 1:
                print("il call")
                #j'ai donc call
                mon_action, en_action =  a,a 
        else :
            is_fold_P1 = False
            is_fold_P2 = False
        return (mon_action, en_action, is_fold_P1, is_fold_P2, partie_continue)
    
def equilibrage_main_T2_print(j,mon_action,mon_nombre_strategie, en_action,en_nombrestrategie, ma_main, ma_combi, en_main, en_combi, mes_jetons, en_jetons) :
    is_fold_P1 = False
    is_fold_P2 = False
    partie_continue = True
    if j%2 == 0 :
        
        if mon_action < en_action :
            if mon_action == mes_jetons :
                print("j'ai all in")
                return (mon_action,en_action,is_fold_P1,is_fold_P2,partie_continue)
            #donc j'ai fold
            print("j'ai fold")
            is_fold_P1 = True
            partie_continue = False
            return (0,en_action, is_fold_P1,is_fold_P2,partie_continue)
        elif mon_action > en_action :
            
            choix1 = prendre_strategie_moyenne(en_nombrestrategie[(en_main, en_combi,mon_action)])[en_action]
            choix2 = 0
            a = min(mon_action, en_jetons)
            if en_action == en_jetons :
                print("il y a eu un all in")
                return (a, a, is_fold_P1, is_fold_P2, partie_continue)
            print(f"il doit raise {a} ou fold") 
            for action in range(a, len(betPossible)) :
                choix2 += prendre_strategie_moyenne(en_nombrestrategie[(en_main, en_combi,mon_action)])[action]
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
    if j%2 == 1 :
        if mon_action > en_action :
            if en_action == en_jetons :
                print("il all in")
                mon_action = en_jetons
                return (mon_action,en_action,is_fold_P1,is_fold_P2,partie_continue)
            #il a donc fold
            print('il fold')
            is_fold_P2, partie_continue = True, False
            return(mon_action, 0, is_fold_P1,is_fold_P2, partie_continue)
        if mon_action < en_action :
            choix1 = prendre_strategie_moyenne(mon_nombre_strategie[(ma_main, ma_combi, en_action)])[mon_action]
            choix2 = 0
            a = min(en_action, mes_jetons)
            if mon_action == mes_jetons :
                print("il y a eu un all in")
                return (a, a, is_fold_P1, is_fold_P2, partie_continue)
            print(f"je dois raise {a} ou fold") 
            for action in range(a, len(betPossible)) :
                choix2 = prendre_strategie_moyenne(mon_nombre_strategie[(ma_main, ma_combi,en_action)])[action]
            choix_call = chv([0 , 1], p = [choix1/(choix1 + choix2), choix2/(choix1 + choix2)])
            if choix_call == 0 :
                print("j'ai fold")
                partie_continue = False
                is_fold_P1 = True 
                mon_action = 1
            elif choix_call == 1:
                print("j'ai call")
                mon_action, en_action = a, a
       
        else :
            is_fold_P1 = False
            is_fold_P2 = False
            partie_continue = True
        return (mon_action, en_action, is_fold_P1, is_fold_P2, partie_continue)
    
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
        mon_action_T1 = 1
    if en_action_T1 == 0 and j%2 == 1:
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
    
    T1 = equilibrage_main_T1_print(j,mon_action_T1,mon_nombre_strat, en_action_T1, en_nombre_strat,PP1, PP2 ,jeton_P1, jeton_P2)
    mon_action_T1, en_action_T1, is_fold_P1, is_fold_P2, partie_continue = T1
    print(f"mon action T1 est : {mon_action_T1}")
    print(f"son action T1 est : {en_action_T1}")
    return (mon_action_T1, en_action_T1, is_fold_P1, is_fold_P2, partie_continue)

def jouer_partie_T2_print(j,ma_main_brut ,ma_combi,ma_decision_T2,mon_action_T1, mon_nombre_strat, en_main_brut ,en_combi,en_decision_T2,en_action_T1, en_nombre_strat,flop, mes_jeton, en_jeton) :
        PP1 = conv_carte_str(ma_main_brut)
        PP2 = conv_carte_str(en_main_brut)
        jeton_P1 = mes_jeton
        jeton_P2 = en_jeton
        #on joue le partie
        mon_action_T2 = ma_decision_T2
        en_action_T2 = en_decision_T2
        
        T2 = equilibrage_main_T2_print(j,ma_decision_T2,mon_nombre_strat, en_action_T2, en_nombre_strat, PP1, ma_combi, PP2, en_combi ,jeton_P1, jeton_P2)
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

def prendre_decision_jeu_T1_print(j,ma_main, mon_nombre_reg, mon_nombre_strat, en_main, en_nombre_reg,en_nombre_strat, jeton_P1, jeton_P2) :
    PP1 = ma_main
    PP2 = en_main
    if j%2 == 0 :
        ma_strategie_T1 = prendre_strategie(mon_nombre_reg[(PP1,-1)])
        #contrairement aux banques moderne, ici on ne peut jouer plus que ce que l'on posséde...
        #plus sérieusement, si notre action est plus grande que nos jetons alors on fait tapis
        #De plus on a obligation de misé dans un tour pair
        mon_action_T1 = max(min(jeton_P1, prendre_decision(ma_strategie_T1)),1)
        en_strategie_T1 = prendre_strategie(en_nombre_reg[(PP2, mon_action_T1)])
        en_action_T1 = min(prendre_decision(en_strategie_T1),jeton_P2)
        for l in range(nombreActions) :
            mon_nombre_strat[(PP1,-1)][l] += ma_strategie_T1[l]
            en_nombre_strat[(PP2,mon_action_T1)][l] += en_strategie_T1[l]
    if j%2 == 1 :
        en_strategie_T1 = prendre_strategie(en_nombre_reg[(PP2,-1)])
        en_action_T1 = max(min(jeton_P2, prendre_decision(en_strategie_T1)),1)
        ma_strategie_T1 = prendre_strategie(mon_nombre_reg[(PP1, en_action_T1)])
        mon_action_T1 = min(prendre_decision(ma_strategie_T1),jeton_P1)
        for l in range(nombreActions) :
            mon_nombre_strat[(PP1,en_action_T1)][l] += ma_strategie_T1[l]
            en_nombre_strat[(PP2,-1)][l] += en_strategie_T1[l]
    print("mon action initiale T1 : " + str(mon_action_T1))
    print("son action initiale T1 : " + str(en_action_T1))
    return (mon_action_T1, en_action_T1)

def prendre_decision_jeu_T2_print(j,ma_main, ma_combi,mon_nombre_strat,mon_nombre_reg, en_main,en_combi, en_nombre_strat,en_nombre_reg, jeton_P1, jeton_P2) :
    PP1 = conv_carte_str(ma_main)
    PP2 = conv_carte_str(en_main)
    if j%2 == 0 :
        en_strategie_T2 = prendre_strategie(en_nombre_reg[(PP2, en_combi,-1)])
        en_action_T2 = min(prendre_decision(en_strategie_T2),jeton_P2)
        ma_strategie_T2 = prendre_strategie(mon_nombre_reg[(PP1, ma_combi,en_action_T2)])
        mon_action_T2 = min(prendre_decision(ma_strategie_T2), jeton_P1)
        for j in range(nombreActions) :
            mon_nombre_strat[(PP1, ma_combi,en_action_T2)][j] += ma_strategie_T2[j]
            en_nombre_strat[(PP2, en_combi,-1)][j] += en_strategie_T2[j]
        print("mon action initiale T2 : " + str(mon_action_T2))
        print("son action initiale T2 : " + str(en_action_T2))
        return (mon_action_T2, en_action_T2)
    if j%2 == 1 :
        ma_strategie_T2 = prendre_strategie(mon_nombre_reg[(PP1, ma_combi,-1)])
        mon_action_T2 = min(prendre_decision(ma_strategie_T2),jeton_P1)
        en_strategie_T2 = prendre_strategie(en_nombre_reg[(PP2, en_combi,mon_action_T2)])
        en_action_T2 = min(prendre_decision(en_strategie_T2), jeton_P2)
        for j in range(nombreActions) :
            mon_nombre_strat[(PP1, ma_combi,-1)][j] += ma_strategie_T2[j]
            en_nombre_strat[(PP2, en_combi,mon_action_T2)][j] += en_strategie_T2[j]
        print("mon action initiale T2 : " + str(mon_action_T2))
        print("son action initiale T2 : " + str(en_action_T2))
        return (mon_action_T2, en_action_T2)