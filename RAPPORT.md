# **Rapport de Projet -- Théorie des Langages et Compilation**

## **Description**

Ce document décrit la répartition des tâches et les problèmes rencontrés par l'equipe PDB.

## **Auteurs**

**Enssat Lannion - Informatique 2**

**Équipe PDB :**

 * Sébastien HERT
 * Alex JOBARD
 * Thomas LEPERCQ
 * Dejan PARIS
 * Adam RIVIERE

## **Répartition des tâches**

Dès le début du projet, nous avons voulu répartir le travail entre tous les membres de l'équipe. Nous avons tout d'abords scindé le projet en deux grosses parties : le compilateur et l'exécuteur.

Thomas LEPERCQ, Alex JOBARD et Dejan PARIS se sont alors penchés sur le compilateur, partie que nous avons jugé plus compliquée, tandis que Sébastien HERT et Adam RIVIERE se sont occupés de l'exécuteur.

Deux parties ont ensuite été distinguées dans le compilateur lui-même. Thomas et Alex ont travaillé sur le fichier [anasyn.py](src/anasyn.py) et en ont produit une copie [anasyn_Table.py](src/anasyn_Table.py) afin d'ajouter les fonctionnalités manquantes. Dejan a utilisé la sortie de [anasyn_Table.py](src/anasyn_Table.py) pour produire le code en *NilNovi*. Une fois l'exécuteur terminé, nous nous sommes tous penchés sur le compilateur et la gestion des erreurs.

## **Problèmes rencontrés**

### **Fusion des différentes parties**

L'organisation que nous avons choisie au sein de l'équipe ainsi que la répartition des tâches ont créés quelques problèmes, notamment au moment où les différentes parties ont été fusionnées. La majorité des problèmes, dans toutes les parties, a été résolue rapidement grâce aux outils de débogage de Python.

Aussi, les codes de [gencode.py](src/gencode.py) et [exec.py](src/exec.py) ont été terminés avant [anasyn_Table.py](src/anasyn_Table.py). Cela nous a contraint à travailler tous ensemble sur ce dernier programme et a légèrement ralentit notre progrès, car seuls Thomas et Alex connaissaient bien le code à ce moment.

### **Déploiement sous Windows**

Afin de fusionner les différentes parties et afin de laisser la possibilité d'utiliser toutes les fonctionnalités, Sébastien a mis au point un script bash. Sous **Linux**, aucun problème à signaler, tant que l'on dispose de python3.

Sous **Windows**, c'est un peu plus problématique : en plus de devoir copier le fichier d'exécution *python.exe* et le renommer en *python3.exe* dans le bon répertoire, il faut parfois changer certaines lignes du script [chef.sh](chef.sh), confer le README du projet. Le plus simple reste d'utiliser une VM **Linux** pour les utilisateurs de Windows.

### **Compilation**

Le problème le plus important au niveau du programme de traduction en *Nilnovi* a été le traitement des modes des paramètres. Au final, les paramètres d'entrée - spécifiés *in* dans le pseudo-code -  acceptent toute expression, mais ceux d'entrée-sortie - *in out* - ne peuvent être qu'une adresse (d'une variable ou d'un paramètre).

Nous voulions au départ indiquer la ligne concernée lors de la détection d'une erreur dans le pseudo-code, mais cela s'est avéré trop complexe. Le dossier [test](test/) contient un exemple pour chaque erreur de pseudo-code détectée par le compilateur.