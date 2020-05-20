#!/bin/bash

#======================chef.sh=====================#

#-----------------------Alias----------------------#

# Compilateur
# Heuristique
# Efficace et
# Fiable

#--------------------------------------------------#


#--------------------Description-------------------#

# Ce script shell permet l'exécution complète du
# compilateur, en prenant en paramètre un fichier
# valide

#--------------------------------------------------#


#----------------------Auteur----------------------#

# Sébastien HERT

#--------------------------------------------------#


#---------------------Fonctions--------------------#

function erreur(){
    stringError="Erreur"


    lenParam=${#stringError}

    lenEq1=$(( ($lenTitle-$lenParam)/2 -1 ))
    lenEq2=$(( $lenTitle-$lenParam-$lenEq1-2 ))
    error=""
    for (( i = 0; i < $lenEq1; i++ )); do
        error="${error}-"
    done
    error="${error} \e[31m\e[1m$stringError\e[0m\e[31m "
    for (( i = 0; i < $lenEq2; i++ )); do
        error="${error}-"
    done

    echo -e "\e[31m${error}"
    echo -e "\e[31m$*"
}

function titre(){
    if [ $# -eq 0 ]; then
        param="Titre"
    else
        param=$*
    fi

    lenParam=${#param}
    lenEq1=$(( ($lenTitle-$lenParam)/2 -1 ))
    lenEq2=$(( $lenTitle-$lenParam-$lenEq1-2 ))
    title=""
    for (( i = 0; i < $lenEq1; i++ )); do
        title="${title}="
    done
    title="${title} $param "
    for (( i = 0; i < $lenEq2; i++ )); do
        title="${title}="
    done

    echo -e "\e[35m\e[1m${title}\n\e[0m"
}

function success(){
    echo -e "\e[32m$*\n\e[0m"
}

function help(){
    echo TODO
}

function verifFichier(){
    #Vérification de la validité du fichier
    if [ ! -f $1 ]; then
        erreur "Le fichier n'est pas valide"
        exit
    fi
}

function tmp(){
    #Création d'un répertoire temporaire
    if [ ! -d tmp ]; then
        mkdir tmp
    fi
}

function table(){
    #Création de la table des identifiants
    titre "Création de la table des identifiants"
    case $1 in
        '-show')
            ./src/anasyn_Table.py $2 --show-ident-table
            echo "";;
        '-file')
            ./src/anasyn_Table.py $2 --show-ident-table >> tmp/IdentTable.txt;;
        *)
            echo error;;
    esac
    success "Création réussie"
}

function liste(){
    #Création de la liste des identifiants
    titre "Création de la liste des identifiants"
    ident_list=$( ./src/anasyn_Table.py $1 --show-ident-list )
    success "Création réussie"
}

function nilnovi(){
    #Création du fichier en langage NilNovi
    titre "Création du programme en NilNovi"
    case $1 in
        '-show')
            ./src/gencode.py $ident_list
            echo "";;
        '-file')
            ./src/gencode.py $ident_list >> tmp/NilNovi.txt;;
        *)
            echo error;;
    esac
    ./src/gencode.py $ident_list >> tmp/NilNovi.txt
    success "Création réussie"
}

function exe(){
    #Exécution du fichier en NilNovi
    titre "Exécution du programme en NilNovi"
    if [ $# -eq 0 ]; then
        ./src/exec.py ./tmp/NilNovi.txt
    elif [ $# -eq 1 ]; then
        ./src/exec.py $1
    else
        echo error
    fi
}

#--------------------------------------------------#


#----------------------Script----------------------#

set -e

lenTitle=50

if [ $1 == '-help' ] || [ $1 == '--help' ] || [ $1 == '-h' ] ; then
    help
fi

titre "Initialisation"

titre "Vérification des paramètres"


#Vérification du nombre de paramètres
if [ $# -eq 0 ]; then
    erreur "Il manque des paramètres"
    echo -e "\e[34msyntaxe attendue :\e[0m ./chef.sh <fichier>\n"
    exit
fi
if [ $# -gt 2 ]; then
    erreur "Trop d'arguments"
    echo -e "\e[34msyntaxe attendue :\e[0m ./chef.sh <fichier>\n"
    exit
fi


#Vérification du paramètre d'exécution
case $1 in
    '-c'|'-complete')
        #Vérification de la validité du fichier
        verifFichier $2

        #Création d'un répertoire temporaire
        tmp

        #Création de la table des identifiants
        table -file $2

        #Création de la liste des identifiants
        ident_list=""
        liste $2

        #Création du fichier en langage NilNovi
        nilnovi -file

        #Exécution du fichier en NilNovi
        exe;;


    '-e'|'-exec')
        #Vérification de la validité du fichier
        verifFichier $2

        #Exécution du fichier en NilNovi
        exe $2;;


    '-t'|'-table')
        #Vérification de la validité du fichier
        verifFichier $2

        #Création de la table des identifiants
        table -show $2;;


    '-nn'|'-nilnovi')
        #Vérification de la validité du fichier
        verifFichier $2

        #Création d'un répertoire temporaire
        tmp

        #Création de la table des identifiants
        table -file $2

        #Création de la liste des identifiants
        ident_list=""
        liste $2

        #Création du fichier en langage NilNovi
        nilnovi -show;;


    *)
        erreur "Le premier paramètre n'a pas été reconnu";;
esac


echo ""
titre "Terminaison"

if [ -d tmp ]; then
    rm -r tmp 
fi

#--------------------------------------------------#


#==================================================#