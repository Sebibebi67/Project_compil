#!/bin/bash


#=================================== test.sh ====================================#


#--------------------------------- Description ----------------------------------#
#
# Test l'intégralité des fichiers de test/nna et test/nnp
#
#--------------------------------------------------------------------------------#


#----------------------------------- Synopsis -----------------------------------#
#
# ./test.sh 
#
#--------------------------------------------------------------------------------#


#----------------------------------- Auteurs ------------------------------------#
#
# Sébastien HERT
#
#--------------------------------------------------------------------------------#


#------------------------------ Variables Globales ------------------------------#

lenTitle=80

#--------------------------------------------------------------------------------#


#---------------------------------- Fonctions -----------------------------------#

function titre(){
    ###
    # Description : Affiche un titre dans le terminal
    #
    # Input :
    # - l'indentifieur pour compléter la ligne
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
        id="="
    elif [ $# -eq 1 ]; then
        param=$1
        id="*"
    elif [ $# -eq 2 ]; then
        param=$2
        id=$1
    else
        echo error
    fi

    lenParam=${#param}
    lenEq1=$(( ($lenTitle-$lenParam)/2 -1 ))
    lenEq2=$(( $lenTitle-$lenParam-$lenEq1-2 ))
    title=""
    for (( i = 0; i < $lenEq1; i++ )); do
        title="${title}$1"
    done
    title="${title} $param "
    for (( i = 0; i < $lenEq2; i++ )); do
        title="${title}$1"
    done

    echo -e "\e[93m\e[1m${title}\n\e[0m"
}

#--------------------------------------------------------------------------------#


#------------------------------------- Main -------------------------------------#

set -e

paths="./test/nna ./test/nnp"


for path in $paths; do
	for file in $(ls $path) ; do
        # echo $file
        if [[ "$file" == "correct"*".nno" ]]; then
            titre '*' "Testing ${path}/${file}"
            ./chef.sh -c $path/$file
        fi
	done
done

# ./chef.sh -c test/nna/error1.nno
# ./chef.sh -c test/nna/error2.nno

#--------------------------------------------------------------------------------#


#================================================================================#

	