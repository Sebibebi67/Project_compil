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


def checkBooleen(identTable, name):
    """
    Description : Vérifie que le paramètre / la variable "name" n'est pas un booléen (pour get()).

    Paramètres :
    - identTable : table des identificateurs
    - name : nom du paramètre / de la variable à tester

    Retour : None

    Auteurs :
    - Sébastien HERT
    - Dejan PARIS
    """
    for e in identTable[::-1] :
        if e[0] == name :
            if e[2] == "boolean" :
                print("Erreur : l'argument " + name + " de get() ne peut pas être un booléen")
                sys.exit(0)



def checkType(identTable, name, scope, type):
    """
    Description : Vérifie que le paramètre / la variable "name" est utilisée conformément à son type.

    Paramètres :
    - identTable : table des identificateurs
    - name : nom du paramètre / de la variable à tester
    - type : type supposé du paramètre / de la variable

    Retour : None

    Auteurs :
    - Sébastien HERT
    - Dejan PARIS
    """
    expectedType = getType(identTable, name, scope)
    if expectedType != type :
        print("Erreur : " + name + " est déclaré comme " + expectedType + ", mais utilisé comme " + type + " !")
        sys.exit(0)



def checkReturnType(identTable, scope, type):
    low_scope = scope
    for e in identTable[::-1] :
        if e[1] < low_scope :
            low_scope = e[1]
        if e[1] == low_scope and e[3] != "null":
            if e[3] != type :
                print("Erreur : la fonction " + e[0] + " doit retourner un " + e[3] + " mais retourne un " + type + " !")
                sys.exit(0)
            return
    print("Erreur : la commande 'return' est utilisée en dehors d'une fonction !")
    sys.exit(0)



def checkDoubleDeclaOp(identTable, name):
    """
    Description : Vérifie que la déclaration d'un paramètre / d'une variable ne fait pas doublon

    Paramètres : None

    Retour : None

    Auteurs :
    - Sébastien HERT
    """
    for e in identTable[::-1] :
        if e[0] == name :
            print("Erreur : " + name + " est déclaré plusieurs fois")
            sys.exit(0)



def checkDoubleDeclaVar(identTable, name, scope):
    """
    Description : Vérifie que la déclaration d'un paramètre / d'une variable ne fait pas doublon

    Paramètres : None

    Retour : None

    Auteurs :
    - Sébastien HERT
    """
    low_scope = scope
    for e in identTable[::-1] :
        if e[1] < low_scope :
            low_scope = e[1]
        if e[1] == low_scope :
            if e[0] == name :
                print("Erreur : " + name + " est déclaré plusieurs fois")
                sys.exit(0)
                


def checkNoDeclaOp(identTable, name):
    """
    Description : Vérifie qu'un paramètre / une variable a été déclaré(e)

    Paramètres : None

    Retour : None

    Auteurs :
    - Sébastien HERT
    """
    defined = False
    for e in identTable[::-1] :
        if e[0] == name :
            defined = True
    if not defined :
        print("Erreur : " + name + " n'est pas déclaré")
        sys.exit(0)



def checkNoDeclaVar(identTable, name, scope):
    """
    Description : Vérifie qu'un paramètre / une variable a été déclaré(e)

    Paramètres : None

    Retour : None

    Auteurs :
    - Sébastien HERT
    """
    defined = False
    low_scope = scope
    for e in identTable[::-1] :
        if e[1] < low_scope :
            low_scope = e[1]
        if e[1] == low_scope :
            if e[0] == name :
                defined = True
    if not defined :
        print("Erreur : " + name + " n'est pas déclaré")
        sys.exit(0)



def getType(identTable, name, scope):
    low_scope = scope
    for e in identTable[::-1] :
        if e[1] < low_scope :
            low_scope = e[1]
        if e[1] == low_scope :
            if e[0] == name :
                return e[2]
    checkNoDeclaVar(identTable, name, scope)



def getReturnType(identTable, name):
    for e in identTable[::-1] :
        if e[0] == name :
            return e[3]
    checkNoDeclaOp(identTable, name)
