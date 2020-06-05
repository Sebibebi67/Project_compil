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
# Dejan PARIS

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
                sys.exit("Erreur : l'argument " + name + " de get() ne peut pas être un booléen\n")



def checkType(identTable, name, scope, type):
    """
    Description : Vérifie que le paramètre / la variable "name" est utilisée conformément à son type.

    Paramètres :
    - identTable : table des identificateurs
    - name : nom du paramètre / de la variable à tester
    - type : type supposé du paramètre / de la variable

    Retour : None

    Appelle :
    - getType

    Auteurs :
    - Sébastien HERT
    - Dejan PARIS
    """
    expectedType = getType(identTable, name, scope)
    if expectedType != type :
        sys.exit("Erreur : " + name + " est déclaré comme " + translate(expectedType) + ", mais utilisé comme " + translate(type) + " !\n")



def checkReturnType(identTable, scope, type):
    """
	Description : Vérifie que "return" est utilisé dans une fonction, et que le type du retour est correct.
	
	Paramètres :
    - identTable : table des identificateurs
    - scope : niveau d'indentation de la fonction
    - type : type supposé du retour
	
	Retour : None
	
	Auteur :
	- Dejan PARIS
	"""
    low_scope = scope
    for e in identTable[::-1] :
        if e[1] < low_scope :
            low_scope = e[1]
        if e[1] == low_scope and e[3] != "null":
            if e[3] != type :
                sys.exit("Erreur : la fonction " + e[0] + " doit retourner un " + translate(e[3]) + " mais retourne un " + translate(type) + " !\n")
            return
    sys.exit("Erreur : la commande 'return' est utilisée en dehors d'une fonction !\n")



def checkDoubleDeclaOp(identTable, name):
    """
    Description : Vérifie que la déclaration d'un paramètre / d'une variable ne fait pas doublon

    Paramètres :
    - identTable : table des identificateurs
    - name : nom du paramètre / de la variable à tester

    Retour : None

    Auteurs :
    - Sébastien HERT
    """
    for e in identTable[::-1] :
        if e[0] == name :
            sys.exit("Erreur : " + name + " est déclaré plusieurs fois\n")



def checkDoubleDeclaVar(identTable, name, scope):
    """
    Description : Vérifie que la déclaration d'un paramètre / d'une variable ne fait pas doublon

    Paramètres :
    - identTable : table des identificateurs
    - name : nom du paramètre / de la variable à tester
    - scope : portée de la variable / du paramètre

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
                sys.exit("Erreur : " + name + " est déclaré plusieurs fois\n")
                


def checkNoDeclaOp(identTable, name):
    """
    Description : Vérifie qu'une procédure / fonction a été déclarée

    Paramètres :
    - identTable : table des identificateurs
    - name : nom de la procédure / fonction à tester

    Retour : None

    Auteurs :
    - Sébastien HERT
    """
    defined = False
    for e in identTable[::-1] :
        if e[0] == name :
            defined = True
    if not defined :
        sys.exit("Erreur : " + name + " n'est pas déclaré\n")



def checkNoDeclaVar(identTable, name, scope):
    """
    Description : Vérifie qu'un paramètre / une variable a été déclaré(e)

    Paramètres :
    - identTable : table des identificateurs
    - name : nom du paramètre / de la variable à tester
    - scope : portée de la variable / du paramètre

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
        sys.exit("Erreur : " + name + " n'est pas déclaré\n")



def getType(identTable, name, scope):
    """
    Description : Renvoie le type d'une variable / d'un paramètre s'il existe

    Paramètres :
    - identTable : table des identificateurs
    - name : nom du paramètre / de la variable à tester
    - scope : portée de la variable / du paramètre

    Retour : 
    - e[2] : type de la variable / du paramètre enregistré dans identTable

    Appelle :
    - checkNoDeclaVar

    Auteurs :
    - Dejan PARIS
    """
    low_scope = scope
    for e in identTable[::-1] :
        if e[1] < low_scope :
            low_scope = e[1]
        if e[1] == low_scope :
            if e[0] == name :
                return e[2]
    checkNoDeclaVar(identTable, name, scope)



def translate(type):
	"""
	Description : Traduit les types pour les messages d'erreur en français.

	Paramètres :
	- type : type à traduire

	Retour :
	- traduction

	Auteurs :
	- Dejan PARIS
	"""
	if type == "integer" :
		return "entier"
	if type == "boolean" :
		return "booléen"
