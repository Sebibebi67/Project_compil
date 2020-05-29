**================ Projet de Théorie des Langages et Compilation =================**

**================================= Description ==================================**

Implémentation d'un compilateur et d'un exécuteur en python, permettant la
compilation d'un programme écrit en pseudo-code en programme NilNovi, avant de
l'exécuter.

**================================= Installation =================================**

Afin de permettre la compilation et l'exécution, il vous faut dans un premier
temps télécharger l'intégralité du dossier.

Vous devez ensuite donner les droits d'exécution aux fichiers suivants :
* chef.sh
* anasyn_Table.py
* gencode.py
* exec.py
Pour cela, dans une terminal Linux, vous pouvez utiliser la commande :
    chmod +x <fichier>

il ne vous reste plus qu'à lancer le script shell chef.sh pour utiliser le
compilateur ou l'exécuteur. Les détails d'utilisation du script sont donnés dans
la partie suivante.

**=================================== Synopsis ===================================**

./chef.sh <arg> <fichier>

arg :
 * -h, -help :       Affiche l'aide
 * -c, -complete :   Compile et exécute un fichier en pseudo-code
 * -e, -exec :       Exécute un fichier Nilnovi
 * -t, -table :      Affiche la table des identifiants à partir d'un fichier
                    écrit en pseudo-code
 * -nn, -nilnovi :   Compile le fichier écrit en pseudo-code et le réécrit en
                    langage NilNovi

fichier :
   Le fichier en pseudo-code ou en NilNovi, en fonction de l'argument 1 choisi

**============================= Erreurs potentielles =============================**

Si vous utilisez windows et que vous rencontrez cette erreur :
    Unknown command "\r$"
vous pouvez utiliser cette commande pour résoudre le problème :
    sed -i 's/\r$//' ./chef.sh

Le fonctionnement est alors strictement identique à celui décrit dans la
section précédente

Si vous utilisez windows et que vous rencontrez une erreur du type :
    bad interpreter: No such file or directory
il vous faudra copier l'exécutable python.exe pour le placer dans le répertoire
/usr/bin

**=================================== Auteurs ====================================**

**Equipe PDB :**

 * Sébastien HERT
 * Alex JOBARD
 * Thomas LEPERCQ
 * Dejan PARIS
 * Adam RIVIERE
