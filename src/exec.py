#!/usr/bin/python

# @package compilateur
# 	Compilateur de langage
#


"""TODO

debutProg();
finProg();
reserver(entier);
empiler(int);
affectation();
valeurPile();
get(); #scan
put(); #print
moins(); #pour l'oppose
sous();
add();
mult();
div();
egal();
diff(); # !=
inf();
infeg();
sup();
supeg();
et();
ou();
non();
tra(int); #goto
tze(int); #goto si faux
erreur(exp); #print exp + return

"""



pile = []
cpt = 0


def debutProg():
    print("Debut de Programme")


def finProg():
    print("Fin de Programme")


def reserver(n):
    for i in range(0, n):
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
            empiler(data)
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
    empiler(int(bool1 & bool2))


def ou():
    # bool1 ou bool2
    bool1 = depiler()
    bool2 = depiler()
    empiler(int(bool1 | bool2))


def non():
    # non boolean
    boolean = depiler()
    empiler(int(not boolean))

# def tra(int):

# def tze(int): #goto si faux
# def erreur(exp): #print exp + return


with open("progTest.txt") as f:
    for line in f:
        eval(line.split(";")[0])
