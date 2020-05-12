#!/usr/bin/python3

#======================exec.py=====================#


#---------------------Encodage---------------------#

# -*- coding: utf-8 -*-

#--------------------------------------------------#


#---------------------Imports----------------------#

import sys

#--------------------------------------------------#


#--------------------Description-------------------#

# Ce fichier gère les potentielles erreurs du code
# donné en paramètre du programme, permettant le bon
# fonctionnement de ce dernier.

#--------------------------------------------------#


#----------------------Auteurs---------------------#

# Sébastien HERT

#--------------------------------------------------#


#----------------Variables globales----------------#



#--------------------------------------------------#


#---------------------Méthodes---------------------#


def checkGetBooleen():
    """
    Description : Vérifie que l'on ne tente pas de récupérer une valeur de booléen

    Paramètres : None

    Retour : None

    Auteurs :
    - Sébastien HERT
    """
    # TODO
    

def checkPutBooleen():
    """
    Description : Vérifie que l'on ne tente pas d'afficher un booléen

    Paramètres : None

    Retour : None

    Auteurs :
    - Sébastien HERT
    """
    # TODO
    

def checkTypage(identTable, name, scope, type):
    """
    Description : Vérifie que les 2 paramètres sont de même type, avant de tenter une affectation

    Paramètres :
    - identTable : table des identificateurs
    - name : nom du paramètre / de la variable à tester
    - scope : portée du paramètre / de la variable
    - type : type supposé du paramètre / de la variable

    Retour : None

    Auteurs :
    - Sébastien HERT
    - Dejan PARIS
    """
    for e in identTable[:-1] :
        if e[0] == name :
            if e[1] == scope :
                if e[3] != type :
                    print("Erreur : " + name + " est déclaré comme " + e[3])
                    sys.exit(0)


def checkIf():
    """
    Description : Vérifie que la condition d'un "if" est valide

    Paramètres : None

    Retour : None

    Auteurs :
    - Sébastien HERT
    """
    # TODO

def checkWhile():
    """
    Description : Vérifie que la condition d'un "while" est valide

    Paramètres : None

    Retour : None

    Auteurs :
    - Sébastien HERT
    """
    # TODO

def checkDoubleDeclaration():
    """
    Description : Vérifie que la déclaration d'une variable ne fait pas doublon

    Paramètres : None

    Retour : None

    Auteurs :
    - Sébastien HERT
    """
    # TODO
