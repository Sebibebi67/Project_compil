#!/usr/bin/python

## 	@package compilateur
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

pile=[]

def empiler(n):
    pile.append(n)
    print(pile.pop())

with open("progTest.txt") as f :
   for line in f :
          (command, end) = line.split("(")
        #   param = end.split(")", 1)[0]
        #   print(command)
        #   print(param)
          if command == "empiler":
            eval(line.split(";")[0])







