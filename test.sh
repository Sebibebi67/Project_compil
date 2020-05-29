#!/bin/bash

set -e

paths="./test/nna ./test/nnp"

for path in $paths; do
	for file in $(ls $path) ; do
		echo -e "\e[93mTesting $path/$file\e[0m\n"
		./chef.sh -c $path/$file
		echo -e "\n"
	done
done	