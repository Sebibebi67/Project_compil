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


#----------------------Script----------------------#

set -e

echo -e "\e[35m\e[1m================ Initialisation ===============\n\e[0m"

echo -e "\e[35m\e[1m========== Vérification du paramètre ==========\n\e[0m"


#Vérification du nombre de paramètres
if [ $# -eq 0 ]; then
    echo -e "\e[31m------Erreur : Il manque le nom de fichier-----\e[0m\n"
    echo -e "\e[34msyntaxe attendue :\e[0m ./chef.sh <fichier>\n"
    exit
fi
if [ $# -gt 1 ]; then
    echo -e "\e[31m---------- \e[1mErreur\e[0m\e[31m - Trop d'arguments ----------\e[0m\n"
    echo -e "\e[34msyntaxe attendue :\e[0m ./chef.sh <fichier>\n"
    exit
fi


#Vérification de la validité du fichier
if [ ! -f $1 ]; then
    echo -e "\e[31m -----\e[1mErreur\e[0m\e[31m : Le fichier n'est pas valide---- \e[0m\n"
    exit
fi


#Création d'un répertoire temporaire
if [ ! -d tmp ]; then
    mkdir tmp
fi

#Création de la liste des identifiants
echo -e "\e[35m\e[1m==== Création de la table des identifiants ====\n\e[0m"
./src/anasyn_Table.py $1 --show-ident-table >> tmp/IdentTable.txt
echo -e "\e[32mCréation réussie\n\e[0m"


#Création de la liste des identifiants
echo -e "\e[35m\e[1m==== Création de la liste des identifiants ====\n\e[0m"
ident_list=$( ./src/anasyn_Table.py $1 --show-ident-list )
echo -e "\e[32mCréation réussie\n\e[0m"

#Création du fichier en langage NilNovi
echo -e "\e[35m\e[1m======= Création du fichier en NilNovi ========\n\e[0m"
./src/gencode.py $ident_list >> tmp/NilNovi.txt
echo -e "\e[32mCréation réussie\n\e[0m"

#Exécution du fichier en NilNovi
echo -e "\e[35m\e[1m======= Exécution du fichier en NilNovi =======\n\e[0m"
./src/exec.py ./tmp/NilNovi.txt

echo -e "\e[35m\e[1m\n================== Terminaison ================\e[0m"
rm -r tmp

#--------------------------------------------------#


#==================================================#
