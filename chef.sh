#!/bin/bash


#=================================== chef.sh ====================================#


#--------------------------------- Description ----------------------------------#
#
# Ce script shell permet l'exécution complète du compilateur, en prenant en
# paramètre un fichier valide.
# 
# Compilateur Habile, Exécuteur Fiable
#
#--------------------------------------------------------------------------------#


#----------------------------------- Synopsis -----------------------------------#
#
# ./chef.sh <arg> <fichier>
#
#--------------------------------------------------------------------------------#


#----------------------------------- Options ------------------------------------#
#
# arg :
#  * -h, -help :       Affiche cette aide
#  * -c, -complete :   Compile et exécute un fichier en pseudo-code
#  * -e, -exec :       Exécute un fichier Nilnovi
#  * -t, -table :      Affiche la table des identifiants à partir d'un fichier
#                     écrit en pseudo-code
#  * -nn, -nilnovi :   Compile le fichier écrit en pseudo-code et le réécrit en
#                     langage NilNovi
#
# fichier : soit un fichier en pseudo-code, soit un fichier en NilNovi, en
# fonction du premier argument choisi
#
#--------------------------------------------------------------------------------#


#----------------------------------- Auteurs ------------------------------------#
#
# Sébastien HERT
#
#--------------------------------------------------------------------------------#


#------------------------------ Variables Globales ------------------------------#
#
lenTitle=80
ident_list=""
# 
#--------------------------------------------------------------------------------#


#---------------------------------- Fonctions -----------------------------------#



function erreur(){
    ###
    # Description : Affiche une erreur dans le terminal
    #
    # Input :
    # - Une chaine de caractères expliquant l'erreur
    #
    # Output :
    # - Affichage dans le terminal
    #
    # Auteur :
    # - Sébastien HERT
    ###

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
    ###
    # Description : Affiche un titre dans le terminal
    #
    # Input :
    # - Le titre sous la forme d'une chaine de caractère
    #
    # Output :
    # - Affichage dans le terminal
    #
    # Auteur :
    # - Sébastien HERT
    ###

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
    ###
    # Description : Affiche un succès dans le terminal
    #
    # Input :
    # - Une chaine de caractère décrivant le succès
    #
    # Output :
    # - Affichage dans le terminal
    #
    # Auteur :
    # - Sébastien HERT
    ###

    echo -e "\e[32m$*\n\e[0m"
}

function help(){
    ###
    # Description : Affiche l'aide
    #
    # Input :
    # - None
    #
    # Output :
    # - Affiche l'aide
    #
    # Authors :
    # - Sébastien HERT
    ###

    titre "Compilateur Habile, Exécuteur Fiable"

    titre "Description"
    echo -e "Cette commande permet l'exécution complète du compilateur, en prenant en"
    echo -e "paramètre un fichier valide.\n"


    titre "Synopsis"
    success "./chef.sh <arg> <fichier>"
    echo -e "arg :"
    echo -e " * -h, -help :       Affiche cette aide"
    echo -e " * -c, -complete :   Compile et exécute un fichier en pseudo-code"
    echo -e " * -e, -exec :       Exécute un fichier Nilnovi"
    echo -e " * -t, -table :      Affiche la table des identifiants à partir d'un fichier"
    echo -e " *                     écrit en pseudo-code"
    echo -e " * -nn, -nilnovi :   Compile le fichier écrit en pseudo-code et le réécrit en"
    echo -e " *                     langage NilNovi"
    echo -e " * -nn, -nilnovi :   Compile le fichier et le réécrit en langage NilNovi\n"

    echo -e "fichier :"
    echo -e "   Le fichier en pseudo-code ou en NilNovi, en fonction de l'argument 1 choisi\n"

    titre "Auteurs"
    success "Equipe PDB :"
    echo -e " * Sébastien HERT"
    echo -e " * Alex JOBARD"
    echo -e " * Thomas LEPERCQ"
    echo -e " * Dejan PARIS"
    echo -e " * Adam RIVIERE\n"

    exit
}

function verifFichier(){
    ###
    # Description : Vérifie la validité du fichier
    #
    # Input :
    # - Le nom du fichier
    #
    # Output :
    # - Une erreur si le fichier n'est pas reconnu
    #
    # Auteur :
    # - Sébastien HERT
    ###

    if [ ! -f $1 ]; then
        erreur "Le fichier n'est pas valide"
        exit
    fi
}

function tmp(){
    ###
    # Description : Crée un répertoire temporaire
    #
    # Input :
    # - None
    #
    # Output :
    # - None
    #
    # Auteur :
    # - Sébastien HERT
    ###

    if [ ! -d tmp ]; then
        mkdir tmp
    fi
}

function table(){
    ###
    # Description : Crée la table des identifiants
    #
    # Input :
    # - -file ou -show indiquant si la sortie est dans un fichier ou afficher dans le terminal
    # - le fichier contenant le pseudo-code
    #
    # Output :
    # - Affichage dans le terminal ou dans un fichier, en fonction de l'argument choisi
    #
    # Auteur :
    # - Sébastien HERT
    ###

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
    ###
    # Description : Crée la liste des identifiants
    #
    # Input :
    # - Le fichier contenant le pseudo-code
    #
    # Output :
    # - Modification d'une variable globale
    #
    # Auteur :
    # - Sébastien HERT
    ###

    titre "Création de la liste des identifiants"
    ident_list=$( ./src/anasyn_Table.py $1 --show-ident-list )
    success "Création réussie"
}

function nilnovi(){
    ###
    # Description : Crée un fichier en langage NilNovi
    #
    # Input :
    # - -file ou -show indiquant si la sortie est dans un fichier ou afficher dans le terminal
    #
    # Output :
    # - Affichage dans le terminal ou dans un fichier, en fonction de l'argument choisi
    #
    # Auteur :
    # - Sébastien HERT
    ###

    titre "Création du programme en NilNovi"
    case $1 in
        '-show')
            ./src/gencode.py $ident_list
            echo "";;
        '-file')
            ./src/gencode.py $ident_list > tmp/NilNovi.txt;;
        *)
            echo error;;
    esac
    # ./src/gencode.py $ident_list > tmp/NilNovi.txt
    success "Création réussie"
}

function exe(){
    ###
    # Description : Exécution du fichier en Nilnovi
    #
    # Input :
    # - Le fichier en NilNovi (par défaut le fichier est .tmp/NilNovi.txt)
    #
    # Output :
    # - Affichage dans le terminal
    #
    # Auteur :
    # - Sébastien HERT
    ###

    titre "Exécution du programme en NilNovi"
    if [ $# -eq 0 ]; then
        ./src/exec.py ./tmp/NilNovi.txt
    elif [ $# -eq 1 ]; then
        ./src/exec.py $1
    else
        echo error
    fi
}

erase(){
    if [ -d tmp ]; then
        rm -r tmp 
    fi
}

#--------------------------------------------------------------------------------#


#------------------------------------- Main -------------------------------------#

set -e

erase

if [[ $1 == '-help' ]] || [[ $1 == '--help' ]] || [[ $1 == '-h' ]] ; then
    help
fi

titre "Initialisation"

titre "Vérification des paramètres"


#Vérification du nombre de paramètres
if [ $# -eq 0 ]; then
    erreur "Il manque des paramètres"
    echo -e "\e[34m\nUtilisez -help pour afficher l'aide :\e[0m ./chef.sh -help\n"
    exit
fi
if [ $# -gt 2 ]; then
    erreur "Trop d'arguments"
    echo -e "\e[34m\nUtilisez -help pour afficher l'aide :\e[0m ./chef.sh -help\n"
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
        liste $2
        echo $ident_list

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
        liste $2

        #Création du fichier en langage NilNovi
        nilnovi -show;;

    *)
        erreur "Le premier paramètre n'a pas été reconnu";;
esac


echo ""
titre "Terminaison"


erase

#--------------------------------------------------------------------------------#


#================================================================================#
