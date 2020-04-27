#!/usr/bin/python

import sys

# @package compilateur
# 	Executeur de langage compile
#

pile = []
cptLigne = 0
pointeurLigne = []


fin = False

programme=[]


def debutProg():
    print("Debut de Programme\n")
    global cptLigne
    cptLigne += 1


def finProg():
    print("\nFin de Programme")
    global fin
    fin = True


def reserver(n):
    global cptLigne
    cpt = cptLigne
    for i in range(0, n):
        empiler(0)
    cptLigne = cpt+1


def empiler(n):
    pile.append(n)
    global cptLigne
    cptLigne += 1


def depiler():
    return pile.pop()


def affectation():
    # a := n
    n = depiler()
    a = depiler()
    global pile
    pile[a] = n
    global cptLigne
    cptLigne += 1


def valeurPile():
    # cherche la valeur a situee a l'adresse n
    global cptLigne
    cpt = cptLigne
    n = depiler()
    a = pile[n]
    empiler(a)
    cptLigne = cpt+1


def get():
    # recupere l'element saisi au clavier
    global cptLigne
    cpt = cptLigne
    ok = False
    while not ok:
        a = input("Entrez un nombre a empiler : ")
        try:
            data = int(a)
            valeurPile()
            empiler(data)
            affectation()
            ok = True
        except ValueError:
            print("Rentrez une valeur entiere")
    cptLigne = cpt+1

def put():
    a = depiler()
    print(a)
    global cptLigne
    cptLigne += 1


def moins():
    global cptLigne
    cpt = cptLigne
    a = depiler()
    empiler(-a)
    cptLigne = cpt+1


def sous():
    # a - b
    global cptLigne
    cpt = cptLigne
    b = depiler()
    a = depiler()
    empiler(a-b)
    cptLigne = cpt+1


def add():
    # a + b
    global cptLigne
    cpt = cptLigne
    b = depiler()
    a = depiler()
    empiler(a+b)
    cptLigne = cpt+1


def mult():
    # a + b
    global cptLigne
    cpt = cptLigne
    b = depiler()
    a = depiler()
    empiler(a*b)
    cptLigne = cpt+1


def div():
    # a//b
    global cptLigne
    cpt = cptLigne
    b = depiler()
    a = depiler()
    empiler(a//b)
    cptLigne = cpt+1


def egal():
    # a == b
    global cptLigne
    cpt = cptLigne
    b = depiler()
    a = depiler()
    empiler(int(a == b))
    cptLigne = cpt+1


def diff():
    # a != b
    global cptLigne
    cpt = cptLigne
    b = depiler()
    a = depiler()
    empiler(int(a != b))
    cptLigne = cpt+1


def inf():
    # a < b
    global cptLigne
    cpt = cptLigne
    b = depiler()
    a = depiler()
    empiler(int(a < b))
    cptLigne = cpt+1


def infeg():
    # a <= b
    global cptLigne
    cpt = cptLigne
    b = depiler()
    a = depiler()
    empiler(int(a <= b))
    cptLigne = cpt+1


def sup():
    # a > b
    global cptLigne
    cpt = cptLigne
    b = depiler()
    a = depiler()
    empiler(int(a > b))
    cptLigne = cpt+1


def supeg():
    # a >= b
    global cptLigne
    cpt = cptLigne
    b = depiler()
    a = depiler()
    empiler(int(a >= b))
    cptLigne = cpt+1


def et():
    # bool1 et bool2
    global cptLigne
    cpt = cptLigne
    bool1 = depiler()
    bool2 = depiler()
    empiler(int(bool1 and bool2))
    cptLigne = cpt+1


def ou():
    # bool1 ou bool2
    global cptLigne
    cpt = cptLigne
    bool1 = depiler()
    bool2 = depiler()
    empiler(int(bool1 or bool2))
    cptLigne = cpt+1


def non():
    # non boolean
    global cptLigne
    cpt = cptLigne
    boolean = depiler()
    empiler(int(not boolean))
    cptLigne = cpt+1


def tra(n):
    global cptLigne 
    cptLigne = n-1


def tze(n):
    # print("tze")
    boolean = depiler()
    global cptLigne 
    if not bool(boolean):
        cptLigne = n-1
    else:
        cptLigne +=1 


def erreur(exp):
    # montre l'erreur et fini le programme
    print(exp)
    print("\nUne Erreur est survenue\nFin de Programme")
    sys.exit()


"""TODO NNP:
    empilerAd(n) -> adresse (var globale)
    empilerParam(n) -> adresse de adresse var locale)
    retourFonc() -> fin Fonc
    retourProc() -> fin proc
    reserverBloc() -> reserve un nouveau bloc en memoire pour l
    traStat(n, t) -> appel ligne n avec t params
"""


def empilerAd(n):
    #empile l'adresse globale n
    empiler(n+pointeurLigne[-1])
    

def empilerParam(n):
    #empile l'adresse locale n
    pile.append(n+pointeurLigne[-1])
    valeurPile()

def retourFonc():
    #fin de fonction
    global pile

    #on sauve la valeur a retourner
    retour = pile.pop()

    #on vide la pile de toutes les potentielles valeurs stockées
    while pile[-1] != None:
        pile.pop()
    
    #on retire le bloc
    for _ in range (3):
        pile.pop()

    #on remet la valeur de retour en sommet de pile
    pile.append(retour)

    #on renvoie à la ligne suivante du programme
    global cptLigne
    pointeurLigne.pop()
    cptLigne = pointeurLigne.pop()

def retourProc():
    #fin de procedure
    
    #on vide la pile de toutes les potentielles valeurs stockées
    while pile[-1] != None:
        pile.pop()
    
    #on retire le bloc
    for _ in range (3):
        pile.pop()

    #on renvoie a la ligne suivante du programme
    global cptLigne
    pointeurLigne.pop()
    cptLigne = pointeurLigne.pop()

def reserverBloc():
    for _ in range(3):
        pile.append(None)

def traStat(n, t):
    #appel de la ligne n avec t paramètre

    #sauvegarde de la prochaine ligne a executer apres le retour de fonction
    global pointeurLigne
    global cptLigne
    pointeurLigne.append(cptLigne+1)

    #deplacement à la ligne n
    cptLigne = n-1

    #stockage du decalage adresse-position dans la pile
    pointeurLigne.append(pile.len()-t)

with open("testFiles/prog2.txt") as f:
    for line in f:
        programme.append(line.split(";")[0])
    while not fin:
        print(cptLigne+1)
        eval(programme[cptLigne])
