#!/usr/bin/python

import sys

# @package compilateur
# 	Compilateur de langage
#

pile = []
cptLigne = 1
cptSaut = 0


def debutProg():
    print("Debut de Programme\n")


def finProg():
    print("\nFin de Programme")


def reserver(n):
    for i in range(0, n):
        print("ok")
        empiler(0)


def empiler(n):
    pile.append(n)


def depiler():
    return pile.pop()


def affectation():
    # a := n
    n = depiler()
    a = depiler()
    a = n
    empiler(a)


def valeurPile():
    # cherche la valeur a situee a l'adresse n
    n = depiler()
    a = pile[n]
    empiler(a)


def get():
    # recupere l'element saisi au clavier
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


def put():
    a = depiler()
    print(a)


def moins():
    a = depiler()
    empiler(-a)


def sous():
    # a - b
    b = depiler()
    a = depiler()
    empiler(a-b)


def add():
    # a + b
    b = depiler()
    a = depiler()
    empiler(a+b)


def mult():
    # a + b
    b = depiler()
    a = depiler()
    empiler(a+b)


def div():
    # a//b
    b = depiler()
    a = depiler()
    empiler(a//b)


def egal():
    # a == b
    b = depiler()
    a = depiler()
    empiler(int(a == b))


def diff():
    # a != b
    b = depiler()
    a = depiler()
    empiler(int(a != b))


def inf():
    # a < b
    b = depiler()
    a = depiler()
    empiler(int(a < b))


def infeg():
    # a <= b
    b = depiler()
    a = depiler()
    empiler(int(a <= b))


def sup():
    # a > b
    b = depiler()
    a = depiler()
    empiler(int(a > b))


def supeg():
    # a >= b
    b = depiler()
    a = depiler()
    empiler(int(a >= b))


def et():
    # bool1 et bool2
    bool1 = depiler()
    bool2 = depiler()
    empiler(int(bool1 and bool2))


def ou():
    # bool1 ou bool2
    bool1 = depiler()
    bool2 = depiler()
    empiler(int(bool1 or bool2))


def non():
    # non boolean
    boolean = depiler()
    empiler(int(not boolean))


def tra(n):
    # print("tra")
    # print(n)
    cptSaut = n


def tze(n):
    # print("tze")
    boolean = depiler()
    if not bool(boolean):
        print("False")
        cptSaut = n


def erreur(exp):
    print(exp)
    sys.exit()


with open("testFiles/prog3.txt") as f:
    for line in f:
        # print(cptLigne)
        # print(cptSaut)
        if cptSaut <= cptLigne:
            eval(line.split(";")[0])
        cptLigne += 1
        # print(pile)
