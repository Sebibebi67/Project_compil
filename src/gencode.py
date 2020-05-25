#!/usr/bin/python3

#======================exec.py=====================#


#---------------------Encodage---------------------#

# -*- coding: utf-8 -*-

#--------------------------------------------------#

#---------------------Imports----------------------#

import sys # Pour récupérer le résultat

#--------------------------------------------------#

#--------------------Description-------------------#

# Ce fichier gère la compilation du pseudo-code
# formaté en langage NilNovi procédural.

#--------------------------------------------------#


#----------------------Auteurs---------------------#

# Dejan PARIS

#--------------------------------------------------#


class Generator(object):
	"""
	Description : Compilateur générant le code NilNovi procédural correspondant à un programme valide en pseudo-code, formaté sous forme de liste, avec la commande :
		g = Generator( [pseudo-code] )
		
	Auteur :
	- Dejan PARIS
	"""

	s = ";\n" 	# Séparateur
	chain = [] 	# Résultat de la compilation
	lines = 2 	# Compteur de lignes du code NilNovi
	id = {}		# Associe les noms de procédures / fonctions à leur numéro de ligne NilNovi
	var = {}  	# Associe les variables à leurs adresses (locales ou globales)
	param = {} 	# Associe les paramètres à leurs adresses locales
	table = []  # Pseudo-code formaté
	proc = [] 	# proc[-1] est "True" si le programme compile une procédure, "False" si c'est une fonction



	def __init__(self, t):
		"""
		Description : Constructeur ; compile le pseudo-code formaté en paramètre et l'affiche.
	
		Paramètres :
		- t : pseudo-code formaté à compiler.
	
		Retour : None
		
		Appelle :
		- generate
		- (printNoLines)
		- (printWithLines)
	
		Auteur :
		- Dejan PARIS
		"""
		self.table = t
		print(t)
		#_, self.chain = self.generate(0, "debutProg()" + self.s)
		# self.printNoLines(self.chain)
		# self.printWithLines(self.chain)



	def generate(self, i, chain):
		"""
		Description : Traduit en code NilNovi une procédure ou une fonction (un programme est géré comme une procédure).
	
		Paramètres :
		- i : la position du début de la procédure / fonction dans le pseudo-code
		- chain : le début du code NilNovi
	
		Retour :
		- i : la position suivant la procédure / fonction
		- chain : le code NilNovi procédural

		Appelle :
		- expression
		- instructions
		- generate

		Auteur :
		- Dejan PARIS
		"""
		paramCount = 0 	# Utilisé pour attribuer des adresses locales aux paramètres et variables
		stock = []  # Stocke temporairement les noms à allouer
		
		while i < len(self.table):
			if self.table[i] == "procedure" or self.table[i] == "function" :
				if self.table[i] == "procedure" :
					self.proc.append(True)
				else :
					self.proc.append(False)
				i += 1
				self.id[self.table[i]] = self.lines 	# Enregistre la procédure / fonction
				i += 1
				
				if self.table[i] == "(" : 	# Paramètres
					
					while not self.table[i] != ")" :
						stock.append(self.table[i])
						i += 3 	# Saute ": [type]" dans le pseudo-code
					i += 1
						
					for k in range(len(stock)):
						self.param[stock[k]] = k 	# Enregistre les paramètres
					paramCount = len(stock)
					stock = []
				
				
			elif self.table[i] == "is":
				i += 1
				
				if self.table[i] == "procedure" or self.table[i] == "function" : # Compilation d'une procédure / fonction
					self.lines += 1 	# Ligne réservée pour "tra"
					i, temp = self.generate(i, "")
					chain += "tra(" + str(self.lines) + ")" + self.s
					chain += temp
				
				while self.table[i] != "begin":  # Déclarations
					stock.append(self.table[i])
					i += 1
					
					if self.table[i] == ":" :
						i += 2 	# Saute ": [type]"
					
				for k in range(len(stock)):
					self.var[stock[k]] = k + paramCount 	# Enregistre les variables
				if len(stock) > 0 : 
					chain += "reserver(" + str(len(stock)) + ")" + self.s
				self.lines += 1
				paramCount = 0
				stock = []
				i += 1 	# Saute "begin"
				
				
			elif self.table[i] != "end":
				i, instr = self.instructions(i)
				chain += instr
			
			
			else :
				if not self.isMain() and self.proc[-1] : 	# Fin de procédure ; le retour des fonctions est géré par "instructions"
					chain += "retourProc()" + self.s
					self.lines += 1
				self.proc.pop()
				self.param = {}
				self.var = {}
				i += 2
				if len(self.proc) == 0 :	# Fin du programme
					chain += "finProg();"
				break
				
		return i, chain



	def instructions(self, i):
		"""
		Description : Traduit en code NilNovi une suite d'instructions non vide.
	
		Paramètres :
		- i : la position du début des instructions dans le pseudo-code
	
		Retour :
		- i : la position suivant les instructions
		- total : le code NilNovi permettant d'exécuter les instructions
		
		Appelle :
		- expression
		- instructions
	
		Auteur :
		- Dejan PARIS
		"""
		total, expr, instr = "", "", "" 	# Utilisés pour l'insertion de "tze" / "tra"
		
		if self.table[i] == "while":
			i += 1
			lines = self.lines 	# Début de la condition (retour de "tra")
			i, expr = self.expression(i)	# Condition
			self.lines += 1 	# Ligne réservée pour "tze"
			while self.table[i] != "end" :
				i, block = self.instructions(i) # Instructions
				instr += block
			expr += "tze(" + str(self.lines+1) + ")" + self.s 	# Saute la boucle si la condition est fausse
			expr += instr
			expr += "tra(" + str(lines) + ")" + self.s 	# Retour à la condition
			self.lines += 1
			i += 1		# Saute "end"
			total += expr
				
				
		elif self.table[i] == "if":
			i += 1
			i, expr = self.expression(i)	# Condition
			self.lines += 1 	# Ligne réservée pour "tze"
			while self.table[i] != "end" and self.table[i] != "else" :
				i, block = self.instructions(i) # Instructions
				instr += block
			expr += "tze(" + str(self.lines) + ")" + self.s 	# Saute les instructions si la condition est fausse
			expr += instr
			instr = ""
			
			if self.table[i] == "else":
				self.lines += 1 	# Ligne réservée pour "tra"
				while self.table[i] != "end" and self.table[i] != "else" :
					i, block = self.instructions(i) 	# Instructions si la condition est fausse
					instr += block
				expr += "tra(" + str(self.lines) + ")" + self.s 	# Saute les instructions si la condition est vraie
				expr += instr
			i += 1		# Saute "end"
			total += expr
			
			
		elif self.table[i] == "put":
			i += 2 	# Saute "("
			i, expr = self.expression(i)
			total += expr
			total += "put()" + self.s
			self.lines += 1
			i += 1 	# Saute ")"
			
			
		elif self.table[i] == "get":
			i += 2 	# Saute "("
			if self.isMain() :
				command = "empiler("
			else :
				command = "empilerAd("
			total += command + str(self.var[self.table[i]]) + ")" + self.s
			total += "get()" + self.s
			self.lines += 2
			i += 2 	# Saute ")"
		
		
		elif self.table[i] in self.id :	# Procédure / Fonction
			call = self.id[self.table[i]]
			paramCount = 0
			total += "reserverBloc()" + self.s
			self.lines += 1
			i += 2 	# Saute "("
			
			while self.table[i] != ")" :
				i, expr = self.expression(i)
				total += expr
				paramCount += 1
				i += 1
			i += 1 	# Saute ")"
			
			total += "traStat(" + str(call) + "," + str(paramCount) + ")" + self.s
			self.lines += 1
		
		
		elif self.table[i] in self.var : # Affectation d'une variable
			if self.isMain() :
				command = "empiler("
			else :
				command = "empilerAd("
			total += command + str(self.var[self.table[i]]) + ")" + self.s
			self.lines += 1
			i += 1
			i, expr = self.expression(i)
			total += expr
			total += "affectation()" + self.s
			self.lines += 1
		
		
		elif self.table[i] in self.param : # Affectation d'un paramètre
			total += "empilerParam(" + str(self.param[self.table[i]]) + ")" + self.s
			self.lines += 1
			i += 1
			i, expr = self.expression(i)
			total += expr
			total += "affectation()" + self.s
			self.lines += 1
		
		
		elif self.table[i] == "return":	# Fin de fonction
			i += 1
			i, expr = self.expression(i)
			total += expr
			total += "retourFonct()" + self.s
			self.lines += 1


		elif self.table[i] == "error": # Message d'erreur
			i += 2 	# Saute "("
			i, expr = self.expression(i)
			total += expr
			total += "erreur()" + self.s
			self.lines += 1
			i += 1 	# Saute ")"
		
		return i, total
		
		
		
	def expression(self, i):
		"""
		Description : Traduit en code NilNovi une expression ou l'union de deux expressions booléennes.
	
		Paramètres :
		- i : la position du début de l'expression dans le pseudo-code
	
		Retour :
		- i : la position suivant l'expression
		- expr+e : le code NilNovi permettant d'empiler la valeur de l'expression
		
		Appelle :
		- exp1
	
		Auteur :
		- Dejan PARIS
		"""
		e = ""
		i, expr = self.exp1(i)
		
		if self.table[i] == "or" :
			i += 1
			i, e = self.exp1(i)
			e += "ou()" + self.s
			self.lines += 1
			
		return i, expr+e
		
		
		
	def exp1(self, i):
		"""
		Description : Traduit en code NilNovi une expression ou l'intersection de deux expressions booléennes.
	
		Paramètres :
		- i : la position du début de l'expression dans le pseudo-code
	
		Retour :
		- i : la position suivant l'expression
		- expr+e : le code NilNovi permettant d'empiler la valeur de l'expression
		
		Appelle :
		- exp2
	
		Auteur :
		- Dejan PARIS
		"""
		e = ""
		i, expr = self.exp2(i)
		
		if self.table[i] == "and" :
			i += 1
			i, e = self.exp2(i)
			e += "et()" + self.s
			self.lines += 1
			
		return i, expr+e
		
		
		
	def exp2(self, i):
		"""
		Description : Traduit en code NilNovi une expression ou la comparaison de deux expressions avec =, /=, >, >=, <, <=.
	
		Paramètres :
		- i : la position du début de l'expression dans le pseudo-code
	
		Retour :
		- i : la position suivant l'expression
		- expr+e : le code NilNovi permettant d'empiler la valeur de l'expression
		
		Appelle :
		- exp3
	
		Auteur :
		- Dejan PARIS
		"""
		e = ""
		i, expr = self.exp3(i)
		
		if self.table[i] == "=" :
			i += 1
			i, e = self.exp3(i)
			e += "egal()" + self.s
			self.lines += 1
			
			
		elif self.table[i] == "/=" :
			i += 1
			i, e = self.exp3(i)
			e += "diff()" + self.s
			self.lines += 1
			
			
		elif self.table[i] == ">" :
			i += 1
			i, e = self.exp3(i)
			e += "sup()" + self.s
			self.lines += 1
			
			
		elif self.table[i] == ">=" :
			i += 1
			i, e = self.exp3(i)
			e += "supeg()" + self.s
			self.lines += 1
			
			
		elif self.table[i] == "<" :
			i += 1
			i, e = self.exp3(i)
			e += "inf()" + self.s
			self.lines += 1
			
			
		elif self.table[i] == "<=" :
			i += 1
			i, e = self.exp3(i)
			e += "infeg()" + self.s
			self.lines += 1
			
		return i, expr+e
		
		
		
	def exp3(self, i):
		"""
		Description : Traduit en code NilNovi une expression ou l'addition / la soustraction de deux expressions.
	
		Paramètres :
		- i : la position du début de l'expression dans le pseudo-code
	
		Retour :
		- i : la position suivant l'expression
		- expr+e : le code NilNovi permettant d'empiler la valeur de l'expression
		
		Appelle :
		- exp4
	
		Auteur :
		- Dejan PARIS
		"""
		e = ""
		i, expr = self.exp4(i)
		
		if self.table[i] == "+" :
			i += 1
			i, e = self.exp4(i)
			e += "add()" + self.s
			self.lines += 1
			
			
		elif self.table[i] == "-" :
			i += 1
			i, e = self.exp4(i)
			e += "sub()" + self.s
			self.lines += 1
			
		return i, expr+e
		
		
		
	def exp4(self, i):
		"""
		Description : Traduit en code NilNovi une expression ou la multiplication / division de deux expressions.
	
		Paramètres :
		- i : la position du début de l'expression dans le pseudo-code
	
		Retour :
		- i : la position suivant l'expression
		- expr+e : le code NilNovi permettant d'empiler la valeur de l'expression
		
		Appelle :
		- prim
	
		Auteur :
		- Dejan PARIS
		"""
		e = ""
		i, expr = self.prim(i)
		
		if self.table[i] == "*" :
			i += 1
			i, e = self.prim(i)
			e += "mult()" + self.s
			self.lines += 1		
			
			
		elif self.table[i] == "/" :
			i += 1
			i, e = self.prim(i)
			e += "div()" + self.s
			self.lines += 1
			
		return i, expr+e
		
		
		
	def prim(self, i):
		"""
		Description : Traduit en code NilNovi une expression composée d'un opérateur primaire (∅, +, -, not) et d'un élément primaire.
	
		Paramètres :
		- i : la position de l'opérateur dans le pseudo-code
	
		Retour :
		- i : la position suivant l'expression
		- expr+e : le code NilNovi permettant d'empiler la valeur de l'expression
		
		Appelle :
		- elemPrim
	
		Auteur :
		- Dejan PARIS
		"""
		e, lines = "", 0
		
		if self.table[i] == "+" :
			i += 1
			
		
		elif self.table[i] == "-" :
			i += 1
			e = "moins()" + self.s
			lines += 1
			
			
		elif self.table[i] == "not" :
			i += 1
			e = "non()" + self.s
			lines += 1
		
		i, expr = self.elemPrim(i)
		self.lines += lines
			
		return i, expr+e
		
		
		
	def elemPrim(self, i):
		"""
		Description : Traduit en code NilNovi une expression ou un élément primaire (booléen, entier, appel à une procédure/fonction, variable ou paramètre).
	
		Paramètres :
		- i : la position de l'élément dans le pseudo-code
	
		Retour :
		- i : la position suivant l'élément
		- expr : le code NilNovi permettant d'empiler l'élément
		
		Appelle :
		- expression
		- instructions
	
		Auteur :
		- Dejan PARIS
		"""
		expr = ""
		
		if self.table[i].isdigit() :	# Entier
			expr += "empiler(" + str(self.table[i]) + ")" + self.s
			self.lines += 1
			i += 1
			
			
		elif self.table[i] == "true" : 	# Booléen
			expr += "empiler(1)" + self.s
			self.lines += 1
			i += 1
			
			
		elif self.table[i] == "false" :
			expr += "empiler(0)" + self.s
			self.lines += 1
			i += 1
			
			
		elif self.table[i] == "(" :	# Expression booléenne
			i += 1
			i, expr = self.expression(i)
			i += 1 	# Saute ")"
			
			
		else :	# Procédure / Fonction / Paramètre / Variable
		
			if self.table[i] in self.id :	# Procédure / Fonction
				i, expr = self.instructions(i) 	# Les appels sont gérés par "instructions"
				
			elif self.table[i] in self.var :	# Variable
				if self.isMain() :
					command = "empiler("
				else :
					command = "empilerAd("
				expr += command + str(self.var[self.table[i]]) + ")" + self.s
				expr += "valeurPile()" + self.s
				self.lines += 2
				i += 1
				
			else : 	# Paramètre
				expr += "empilerParam(" + str(self.var[self.table[i]]) + ")" + self.s
				expr += "valeurPile()" + self.s
				self.lines += 2
				i += 1
				
		return i, expr
		
		
		
	def printNoLines(self, chain):
		"""
		Description : Affiche le résultat de la compilation, tel qu'exploité par l'exécuteur, sans numéro de ligne.
	
		Paramètres :
		- chain : le code NilNovi à afficher
	
		Retour : None
	
		Auteur :
		- Dejan PARIS
		"""
		table = chain.split("\n")
		for l in range(self.lines):
			print(table[l])
		
		
		
	def printWithLines(self, chain):
		"""
		Description : Affiche le résultat de la compilation, tel qu'exploité par l'exécuteur, avec les numéros de lignes commençant à 1.
	
		Paramètres :
		- chain : le code NilNovi à afficher
	
		Retour : None
	
		Auteur :
		- Dejan PARIS
		"""
		table = chain.split("\n")
		space = "  "
		for l in range(self.lines):
			if l >= 9 : space = " "
			print(str(l+1) + space + table[l])
			
			
			
	def isMain(self):
		"""
		Description : Indique si la procédure en cours de compilation est le programme principal.
	
		Paramètres : None
	
		Retour :
		- booléen
	
		Auteur :
		- Dejan PARIS
		"""
		return len(self.proc) == 1
		
		
		
		

#--------------------------------------------------#


#-----------------------Main-----------------------#

table = sys.argv[1].split(";")
# print(table)
g = Generator(table)
print(g.chain)

#--------------------------------------------------#


#==================================================#
