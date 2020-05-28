#!/usr/bin/python3

# -*- coding: utf-8 -*-

## 	@package anasyn
# 	Syntactical Analyser package. 
#

########################################################################				 	
#### TO DO
# Completer la list (listeIdentificateur) avec les indentificateurs necessaires
# Une fois completee, la parse a nouveau pour creer la table (plus simple)
####
########################################################################

import sys, argparse, re
import logging
from erreur import *
import analex

logger = logging.getLogger('anasyn')

DEBUG = False
LOGGING_LEVEL = logging.DEBUG

"""
Description : Déclarations globales utiles

Paramètres : None

Retour : None

Auteurs :
- Alex JOBARD, Thomas LEPERCQ
"""
listeIdentificateur = []
tableIdentificateur = []
porteeActuelle = 0
indiceValeurAffectation = None 	# UNFINISHED / UNUSED
valeurAffectee = []				# UNFINISHED / UNUSED

class AnaSynException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
                return repr(self.value)

########################################################################				 	
#### Syntactical Diagrams
########################################################################				 	

def program(lexical_analyser):
	specifProgPrinc(lexical_analyser)
	lexical_analyser.acceptKeyword("is")
	ajoutIdentificateur("is")
	corpsProgPrinc(lexical_analyser)
	
def specifProgPrinc(lexical_analyser):
	lexical_analyser.acceptKeyword("procedure")
	ajoutIdentificateur("procedure")
	ident = lexical_analyser.acceptIdentifier()
	logger.debug("Name of program : "+ident)
	ajoutIdentificateur(str(ident),"corps")

def  corpsProgPrinc(lexical_analyser):
	if not lexical_analyser.isKeyword("begin"):
		logger.debug("Parsing declarations")
		partieDecla(lexical_analyser)
		logger.debug("End of declarations")
	lexical_analyser.acceptKeyword("begin")
	ajoutIdentificateur("begin")

	if not lexical_analyser.isKeyword("end"):
		logger.debug("Parsing instructions")
		suiteInstr(lexical_analyser)
		logger.debug("End of instructions")
			
	lexical_analyser.acceptKeyword("end")
	ajoutIdentificateur("end","end")
	lexical_analyser.acceptFel()
	logger.debug("End of program")
	
def partieDecla(lexical_analyser):
        if lexical_analyser.isKeyword("procedure") or lexical_analyser.isKeyword("function") :
                listeDeclaOp(lexical_analyser)
                if not lexical_analyser.isKeyword("begin"):
                        listeDeclaVar(lexical_analyser)
        
        else:
                listeDeclaVar(lexical_analyser)                

def listeDeclaOp(lexical_analyser):
	declaOp(lexical_analyser)
	lexical_analyser.acceptCharacter(";")
	if lexical_analyser.isKeyword("procedure") or lexical_analyser.isKeyword("function") :
		listeDeclaOp(lexical_analyser)

def declaOp(lexical_analyser):
	if lexical_analyser.isKeyword("procedure"):
		procedure(lexical_analyser)
	if lexical_analyser.isKeyword("function"):
		fonction(lexical_analyser)

def procedure(lexical_analyser):
	lexical_analyser.acceptKeyword("procedure")
	ajoutIdentificateur("procedure")
	ident = lexical_analyser.acceptIdentifier()
	logger.debug("Name of procedure : "+ident)
	ajoutIdentificateur(str(ident),"corps")
       
	partieFormelle(lexical_analyser)

	lexical_analyser.acceptKeyword("is")
	ajoutIdentificateur("is")
	corpsProc(lexical_analyser)
       

def fonction(lexical_analyser):
	lexical_analyser.acceptKeyword("function")
	ident = lexical_analyser.acceptIdentifier()
	logger.debug("Name of function : "+ident)
	ajoutIdentificateur(str(ident),"corps")
	
	partieFormelle(lexical_analyser)

	lexical_analyser.acceptKeyword("return")
	nnpType(lexical_analyser)
        
	lexical_analyser.acceptKeyword("is")
	ajoutIdentificateur("is")
	corpsFonct(lexical_analyser)

def corpsProc(lexical_analyser):
	if not lexical_analyser.isKeyword("begin"):
		partieDeclaProc(lexical_analyser)
	lexical_analyser.acceptKeyword("begin")
	ajoutIdentificateur("begin")
	suiteInstr(lexical_analyser)
	lexical_analyser.acceptKeyword("end")
	ajoutIdentificateur("end","end")

def corpsFonct(lexical_analyser):
	if not lexical_analyser.isKeyword("begin"):
		partieDeclaProc(lexical_analyser)
	lexical_analyser.acceptKeyword("begin")
	suiteInstrNonVide(lexical_analyser)
	lexical_analyser.acceptKeyword("end")

def partieFormelle(lexical_analyser):
	lexical_analyser.acceptCharacter("(")
	ajoutIdentificateur("(")
	if not lexical_analyser.isCharacter(")"):
		listeSpecifFormelles(lexical_analyser)
	lexical_analyser.acceptCharacter(")")
	ajoutIdentificateur(")")

def listeSpecifFormelles(lexical_analyser):
	specif(lexical_analyser)
	if not lexical_analyser.isCharacter(")"):
		lexical_analyser.acceptCharacter(";")
		listeSpecifFormelles(lexical_analyser)

def specif(lexical_analyser):
	listeIdent(lexical_analyser)
	lexical_analyser.acceptCharacter(":")
	if lexical_analyser.isKeyword("in"):
		mode(lexical_analyser)
                
	nnpType(lexical_analyser)

def mode(lexical_analyser):
	lexical_analyser.acceptKeyword("in")
	if lexical_analyser.isKeyword("out"):
		lexical_analyser.acceptKeyword("out")
		logger.debug("in out parameter")                
	else:
		logger.debug("in parameter")

def nnpType(lexical_analyser):
	if lexical_analyser.isKeyword("integer"):
		lexical_analyser.acceptKeyword("integer")
		ajoutIdentificateur(":")
		ajoutIdentificateur("integer","type")
		logger.debug("integer type")
	elif lexical_analyser.isKeyword("boolean"):
		lexical_analyser.acceptKeyword("boolean")
		logger.debug("boolean type")  
		ajoutIdentificateur(":")
		ajoutIdentificateur("boolean","type")              
	else:
		logger.error("Unknown type found <"+ lexical_analyser.get_value() +">!")
		raise AnaSynException("Unknown type found <"+ lexical_analyser.get_value() +">!")

def partieDeclaProc(lexical_analyser):
	listeDeclaVar(lexical_analyser)

def listeDeclaVar(lexical_analyser):
	declaVar(lexical_analyser)
	if lexical_analyser.isIdentifier():
		listeDeclaVar(lexical_analyser)

def declaVar(lexical_analyser):
	listeIdent(lexical_analyser)
	lexical_analyser.acceptCharacter(":")
	logger.debug("now parsing type...")
	nnpType(lexical_analyser)
	lexical_analyser.acceptCharacter(";")

def listeIdent(lexical_analyser):
	ident = lexical_analyser.acceptIdentifier()
	ajoutIdentificateur(str(ident),"variable")
	logger.debug("identifier found: "+str(ident))

	if lexical_analyser.isCharacter(","):
		lexical_analyser.acceptCharacter(",")
		listeIdent(lexical_analyser)

def suiteInstrNonVide(lexical_analyser):
	instr(lexical_analyser)
	if lexical_analyser.isCharacter(";"):
		lexical_analyser.acceptCharacter(";")
		suiteInstr(lexical_analyser)

def suiteInstr(lexical_analyser):
	if not lexical_analyser.isKeyword("end"):
		suiteInstrNonVide(lexical_analyser)

def instr(lexical_analyser):		
	if lexical_analyser.isKeyword("while"):
		ajoutIdentificateur("while","corps")
		boucle(lexical_analyser)
	elif lexical_analyser.isKeyword("if"):
		ajoutIdentificateur("if","corps")
		altern(lexical_analyser)
	elif lexical_analyser.isKeyword("get") or lexical_analyser.isKeyword("put"):
		es(lexical_analyser)
	elif lexical_analyser.isKeyword("return"):
		ajoutIdentificateur("return")
		retour(lexical_analyser)
	elif lexical_analyser.isIdentifier():
		saveIdent = str(lexical_analyser.get_value())
		ident = lexical_analyser.acceptIdentifier()
		# if lexical_analyser.isCharacter("("):
		#   # ERREUR AVEC LE ELIF "(" SUIVANT
		# 	ajoutIdentificateur(saveIdent)
		# 	ajoutIdentificateur("(")
		# 	ajoutIdentificateur(")")
		if lexical_analyser.isSymbol(":="):
			# affectation
			ajoutIdentificateur(saveIdent,"affectation")
			lexical_analyser.acceptSymbol(":=")
			expression(lexical_analyser)
			logger.debug("parsed affectation")
			# ajoutIdentificateur(None,"finAffectation")
		elif lexical_analyser.isCharacter("("):
			ajoutIdentificateur(saveIdent)
			lexical_analyser.acceptCharacter("(")
			ajoutIdentificateur("(")
			if not lexical_analyser.isCharacter(")"):
				listePe(lexical_analyser)

			lexical_analyser.acceptCharacter(")")
			ajoutIdentificateur(")")
			logger.debug("parsed procedure call")
		else:
			logger.error("Expecting procedure call or affectation!")
			raise AnaSynException("Expecting procedure call or affectation!")
		
	else:
		logger.error("Unknown Instruction <"+ lexical_analyser.get_value() +">!")
		raise AnaSynException("Unknown Instruction <"+ lexical_analyser.get_value() +">!")

def listePe(lexical_analyser):
	expression(lexical_analyser)
	if lexical_analyser.isCharacter(","):
		lexical_analyser.acceptCharacter(",")
		listePe(lexical_analyser)

def expression(lexical_analyser):
	logger.debug("parsing expression: " + str(lexical_analyser.get_value()))
	validCondition = exp1(lexical_analyser)
	if lexical_analyser.isKeyword("or"):
		lexical_analyser.acceptKeyword("or")
		validConditionOr = exp1(lexical_analyser)
		return validCondition and validConditionOr
	return validCondition
        
def exp1(lexical_analyser):
	logger.debug("parsing exp1")
	
	validCondition = exp2(lexical_analyser)
	if lexical_analyser.isKeyword("and"):
		lexical_analyser.acceptKeyword("and")
		validConditionAnd = exp2(lexical_analyser)
		return validCondition and validConditionAnd
	return validCondition
		
        
def exp2(lexical_analyser):
	logger.debug("parsing exp2")
        
	validCondition = exp3(lexical_analyser)
	if	lexical_analyser.isSymbol("<") or \
		lexical_analyser.isSymbol("<=") or \
		lexical_analyser.isSymbol(">") or \
		lexical_analyser.isSymbol(">=") or \
		lexical_analyser.isSymbol("=") or \
		lexical_analyser.isSymbol("/="):
		opRel(lexical_analyser)
		validConditionComp = exp3(lexical_analyser)
		return not validCondition and not validConditionComp	# comparing two integers
	return validCondition
	
def opRel(lexical_analyser):
	logger.debug("parsing relationnal operator: " + lexical_analyser.get_value())
        
	if	lexical_analyser.isSymbol("<"):
		lexical_analyser.acceptSymbol("<")
        
	elif lexical_analyser.isSymbol("<="):
		lexical_analyser.acceptSymbol("<=")
        
	elif lexical_analyser.isSymbol(">"):
		lexical_analyser.acceptSymbol(">")
        
	elif lexical_analyser.isSymbol(">="):
		lexical_analyser.acceptSymbol(">=")
        
	elif lexical_analyser.isSymbol("="):
		lexical_analyser.acceptSymbol("=")
        
	elif lexical_analyser.isSymbol("/="):
		lexical_analyser.acceptSymbol("/=")
        
	else:
		msg = "Unknown relationnal operator <"+ lexical_analyser.get_value() +">!"
		logger.error(msg)
		raise AnaSynException(msg)

def exp3(lexical_analyser):
	logger.debug("parsing exp3")
	validCondition = exp4(lexical_analyser)	
	if lexical_analyser.isCharacter("+") or lexical_analyser.isCharacter("-"):
		opAdd(lexical_analyser)
		validConditionAdd = exp4(lexical_analyser)
		return not validCondition and not validConditionAdd		# operating on two integers
	return validCondition

def opAdd(lexical_analyser):
	logger.debug("parsing additive operator: " + lexical_analyser.get_value())
	if lexical_analyser.isCharacter("+"):
		lexical_analyser.acceptCharacter("+")
                
	elif lexical_analyser.isCharacter("-"):
		lexical_analyser.acceptCharacter("-")
                
	else:
		msg = "Unknown additive operator <"+ lexical_analyser.get_value() +">!"
		logger.error(msg)
		raise AnaSynException(msg)

def exp4(lexical_analyser):
	logger.debug("parsing exp4")
        
	validCondition = prim(lexical_analyser)	
	if lexical_analyser.isCharacter("*") or lexical_analyser.isCharacter("/"):
		opMult(lexical_analyser)
		validConditionMult = prim(lexical_analyser)
		return not validCondition and not validConditionMult	# operating on two integers
	return validCondition

def opMult(lexical_analyser):
	logger.debug("parsing multiplicative operator: " + lexical_analyser.get_value())
	if lexical_analyser.isCharacter("*"):
		lexical_analyser.acceptCharacter("*")
                
	elif lexical_analyser.isCharacter("/"):
		lexical_analyser.acceptCharacter("/")
                
	else:
		msg = "Unknown multiplicative operator <"+ lexical_analyser.get_value() +">!"
		logger.error(msg)
		raise AnaSynException(msg)

def prim(lexical_analyser):
	logger.debug("parsing prim")
        
	if lexical_analyser.isCharacter("+") or lexical_analyser.isCharacter("-") or lexical_analyser.isKeyword("not"):
		opUnaire(lexical_analyser)
	return elemPrim(lexical_analyser)

def opUnaire(lexical_analyser):
	logger.debug("parsing unary operator: " + lexical_analyser.get_value())
	ajoutIdentificateur(str(lexical_analyser.get_value()))
	if lexical_analyser.isCharacter("+"):
		lexical_analyser.acceptCharacter("+")
                
	elif lexical_analyser.isCharacter("-"):
		lexical_analyser.acceptCharacter("-")
                
	elif lexical_analyser.isKeyword("not"):
		lexical_analyser.acceptKeyword("not")
                
	else:
		msg = "Unknown additive operator <"+ lexical_analyser.get_value() +">!"
		logger.error(msg)
		raise AnaSynException(msg)

def elemPrim(lexical_analyser):
	logger.debug("parsing elemPrim: " + str(lexical_analyser.get_value()))
	ajoutIdentificateur(str(lexical_analyser.get_value()),"valeurAffectee")
	if lexical_analyser.isCharacter("("):
		lexical_analyser.acceptCharacter("(")
		validCondition = expression(lexical_analyser)
		lexical_analyser.acceptCharacter(")")
		return validCondition
	elif lexical_analyser.isInteger() or lexical_analyser.isKeyword("true") or lexical_analyser.isKeyword("false"):
		return valeur(lexical_analyser) == "boolean"
	elif lexical_analyser.isIdentifier():
		ident = lexical_analyser.acceptIdentifier()
		if lexical_analyser.isCharacter("("):			# Appel fonct
			lexical_analyser.acceptCharacter("(")
			if not lexical_analyser.isCharacter(")"):
				listePe(lexical_analyser)

			lexical_analyser.acceptCharacter(")")
			logger.debug("parsed procedure call")

			logger.debug("Call to function: " + ident)
			return True		# TODO type du retour
		else:
			logger.debug("Use of an identifier as an expression: " + ident)
			if not lexical_analyser.isCharacter(")"):
				ajoutIdentificateur(str(lexical_analyser.get_value()),"valeurAffectee")
			return getType(ident) == "boolean"
	else:
		logger.error("Unknown Value!")
		raise AnaSynException("Unknown Value!")

def valeur(lexical_analyser):
	if lexical_analyser.isInteger():
		entier = lexical_analyser.acceptInteger()
		logger.debug("integer value: " + str(entier))
		return "integer"
	elif lexical_analyser.isKeyword("true") or lexical_analyser.isKeyword("false"):
		return valBool(lexical_analyser)
	else:
		logger.error("Unknown Value! Expecting an integer or a boolean value!")
		raise AnaSynException("Unknown Value ! Expecting an integer or a boolean value!")

def valBool(lexical_analyser):
	if lexical_analyser.isKeyword("true"):
		lexical_analyser.acceptKeyword("true")	
		logger.debug("boolean true value")
                
	else:
		logger.debug("boolean false value")
		lexical_analyser.acceptKeyword("false")	
        
	return "boolean"

def getType(ident):
    for e in tableIdentificateur[:-1] :
        if e[0] == ident :
            return e[2]

def es(lexical_analyser):
	logger.debug("parsing E/S instruction: " + lexical_analyser.get_value())
	if lexical_analyser.isKeyword("get"):
		lexical_analyser.acceptKeyword("get")
		ajoutIdentificateur("get","getput")
		ajoutIdentificateur("(")
		lexical_analyser.acceptCharacter("(")
		ident = lexical_analyser.acceptIdentifier()
		ajoutIdentificateur(str(ident))
		ajoutIdentificateur(")")
		lexical_analyser.acceptCharacter(")")
		logger.debug("Call to get "+ident)
	elif lexical_analyser.isKeyword("put"):
		lexical_analyser.acceptKeyword("put")
		ajoutIdentificateur("put","getput")
		ajoutIdentificateur("(")
		lexical_analyser.acceptCharacter("(")
		expression(lexical_analyser)
		lexical_analyser.acceptCharacter(")")
		ajoutIdentificateur(")")
		logger.debug("Call to put")
	else:
		logger.error("Unknown E/S instruction!")
		raise AnaSynException("Unknown E/S instruction!")

def boucle(lexical_analyser):
	logger.debug("parsing while loop: ")
	lexical_analyser.acceptKeyword("while")

	if not expression(lexical_analyser) :
		logger.error("Invalid condition : expression is not a boolean !")
		raise AnaSynException("Invalid condition : expression is not a boolean !")

	lexical_analyser.acceptKeyword("loop")
	suiteInstr(lexical_analyser)

	lexical_analyser.acceptKeyword("end")
	ajoutIdentificateur("end","end")
	logger.debug("end of while loop ")

def altern(lexical_analyser):
	logger.debug("parsing if: ")
	lexical_analyser.acceptKeyword("if")

	if not expression(lexical_analyser) :
		logger.error("Invalid condition : expression is not a boolean !")
		raise AnaSynException("Invalid condition : expression is not a boolean !")
       
	lexical_analyser.acceptKeyword("then")
	suiteInstr(lexical_analyser)

	if lexical_analyser.isKeyword("else"):
		lexical_analyser.acceptKeyword("else")
		ajoutIdentificateur("else","corps")
		suiteInstr(lexical_analyser)
       
	lexical_analyser.acceptKeyword("end")
	ajoutIdentificateur("end","end")
	logger.debug("end of if")

def retour(lexical_analyser):
	logger.debug("parsing return instruction")
	lexical_analyser.acceptKeyword("return")
	expression(lexical_analyser)

########################################################################

"""
Description : méthode appelée pour construire la table d'identificateurs

Paramètres : identificateur, tableOperation

Retour : None

Auteurs :
- Alex JOBARD, Thomas LEPERCQ
"""	
def ajoutIdentificateur(identificateur,tableOperation = "None"):
	global listeIdentificateur		# Liste pour gencode.py
	global tableIdentificateur		# Table d'identificateurs
	global porteeActuelle 			# Scope
	global indiceValeurAffectation 	# UNFINISHED / UNUSED
	global valeurAffectee			# UNFINISHED / UNUSED

	if(identificateur != None): 		# case finAffectation (UNFINISHED / UNUSED)
		listeIdentificateur.append(identificateur)
	
	if(tableOperation == "None"):
		return
	elif(tableOperation == "corps"): 	# Identificateur d'une procédure, fonction ou boucle
		if(identificateur != "else"):	# Le scope ne change pas entre un if et le else correspondant
			porteeActuelle += 1
		tableIdentificateur.append([identificateur])
		tableIdentificateur[-1].append(porteeActuelle)
		tableIdentificateur[-1].append("corps")
		tableIdentificateur[-1].append(None)

	elif(tableOperation == "variable"): # Identificateur d'une variable
		tableIdentificateur.append([identificateur])
		tableIdentificateur[-1].append(porteeActuelle)
		tableIdentificateur[-1].append("null")
		tableIdentificateur[-1].append(None)
	
	elif(tableOperation == "type"):		# Type d'une variable déjà déclarée
		portee = tableIdentificateur[-1][1]
		i = 0
		while(tableIdentificateur[-1-i][1] == portee and tableIdentificateur[-1-i][2] == "null"):
			tableIdentificateur[-1-i][2] = identificateur
			l = len(tableIdentificateur)
			i += 1
			if(i > l-1):
				break

	elif(tableOperation == "getput"):	# Identificateur d'un appel à put ou get
		tableIdentificateur.append([identificateur])
		tableIdentificateur[-1].append(porteeActuelle)
		tableIdentificateur[-1].append("getput")
		tableIdentificateur[-1].append(None)

	elif(tableOperation == "end"):		# Gestion du scope à la fin d'une procédure, fonction ou boucle
		porteeActuelle -= 1

	################# UNFINISHED - UNUSED ################# 
	"""
	Description : Calcul des valeurs finales des variables déclarées

	Paramètres : indentificateur

	Retour : valeur finale de la variable dans la derniere colonne
	de la table des identificateurs

	Auteurs :
	- Thomas LEPERCQ
	"""
	# elif(tableOperation == "affectation"):
	# 	i = 0
	# 	while(tableIdentificateur[i][0] != identificateur):
	# 		i += 1
	# 	indiceValeurAffectation = i

	# elif(tableOperation == "valeurAffectee"):
	# 	if(indiceValeurAffectation != None):
	# 		valeurAffectee.append(identificateur)

	# elif(tableOperation == "finAffectation"):
	# 	evaluation = ""
	# 	for i in range(len(valeurAffectee)):
	# 		for j in range(len(tableIdentificateur)):
	# 			if(valeurAffectee[i] == tableIdentificateur[j][0]):
	# 				if(tableIdentificateur[j][-1] == None):
	# 					valeurAffectee[i] = str(0)
	# 				else:
	# 					valeurAffectee[i] = str(tableIdentificateur[j][-1])
	# 		evaluation += valeurAffectee[i]
	# 	tableIdentificateur[indiceValeurAffectation][-1] = eval(evaluation)
	# 	indiceValeurAffectation = None
	# 	valeurAffectee = []

########################################################################
def main():
	parser = argparse.ArgumentParser(description='Do the syntactical analysis of a NNP program.')
	parser.add_argument('inputfile', type=str, nargs=1, help='name of the input source file')
	parser.add_argument('-o', '--outputfile', dest='outputfile', action='store', \
                default="", help='name of the output file (default: stdout)')
	parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
	parser.add_argument('-d', '--debug', action='store_const', const=logging.DEBUG, \
                default=logging.INFO, help='show debugging info on output')
	parser.add_argument('-p', '--pseudo-code', action='store_const', const=True, default=False, \
                help='enables output of pseudo-code instead of assembly code')
	parser.add_argument('--show-ident-table', action='store_true', \
                help='shows the final identifiers table')
	parser.add_argument('--show-ident-list', action='store_true', \
                help='shows the identifiers list used in gencode.py')
	args = parser.parse_args()

	filename = args.inputfile[0]
	f = None
	try:
		f = open(filename, 'r')
	except:
		print("Error: can\'t open input file!")
		return
		
	outputFilename = args.outputfile
	
  	# create logger      
	LOGGING_LEVEL = args.debug
	logger.setLevel(LOGGING_LEVEL)
	ch = logging.StreamHandler()
	ch.setLevel(LOGGING_LEVEL)
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	ch.setFormatter(formatter)
	logger.addHandler(ch)

	if args.pseudo_code:
		True#
	else:
		False#

	lexical_analyser = analex.LexicalAnalyser()
	
	lineIndex = 0
	for line in f:
		line = line.rstrip('\r\n')
		lexical_analyser.analyse_line(lineIndex, line)
		lineIndex = lineIndex + 1
	f.close()
	

	# launch the analysis of the program
	lexical_analyser.init_analyser()
	program(lexical_analyser)
	
	"""
	Description : Gestion des arguments pour l'exécution

	Paramètres : args

	Retour : Table des identificateurs ou liste donnée à gencode.py

	Auteurs :
	- Alex JOBARD
	"""
	if args.show_ident_table:
		for i in range(len(tableIdentificateur)):
			print(tableIdentificateur[i])

	if args.show_ident_list:
		ident_list=""
		for i in range(len(listeIdentificateur)):
			ident_list=ident_list+listeIdentificateur[i]+";"
			# print(listeIdentificateur[i]+";")
		print(ident_list)

	if outputFilename != "":
			try:
					output_file = open(outputFilename, 'w')
			except:
					print("Error: can\'t open output file!")
					return
	else:
			output_file = sys.stdout

	# Outputs the generated code to a file
	#instrIndex = 0
	#while instrIndex < codeGenerator.get_instruction_counter():
	#        output_file.write("%s\n" % str(codeGenerator.get_instruction_at_index(instrIndex)))
	#        instrIndex += 1
		
	if outputFilename != "":
			output_file.close() 

########################################################################				 

if __name__ == "__main__":
    main() 