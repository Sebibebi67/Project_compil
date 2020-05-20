#!/bin/bash

#compilateur heuristique efficace et fiable

# echo $1

rm -r tmp
mkdir tmp

python src/anasyn_Table.py $1 --show-ident-table >> tmp/IdentTable.txt

ident_list=$( python src/anasyn_Table.py $1 --show-ident-list )
# echo $ident_list

./src/gencode.py $ident_list >> tmp/NilNovi.txt

./src/exec.py ./tmp/NilNovi.txt