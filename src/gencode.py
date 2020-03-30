## This function translates *valid* pseudo code (see examples) into NilNovi Object code. It does not consider grammatical errors, those must be treated before this code is run.

class Generator(object)
	
	s = ";\n"	# separator
	chain = "debutProg()" + s 	# NilNovi Object code
	stock = []	# temporarily stores names to allocate
	id = {}		# associates identifiers to their line number
	var = {}	# associates variables to their type
	table = []	# pseudo code
		
	# The constructor
	def __init__(self, t):
		self.table = t
	
	# Main function
	def generate():
		type = {"integer" : 0,
				"boolean" : 1}
		i = 0 	# current line
		while i < len(table) :
			instr = ""
			w = table[i]	# current word
			if w == "procedure" :
				i++
				id[table[i]] = i 	# stores procedure identifier
				i++
			elif w == "is" :
				i++
				while not table[i] == "begin" :	# declarations
					stock.append(table[i])	# stores first variable
					i++
					while table[i] == "," :	# there are several variables of the same type
						i++
						stock.append(table[i])	# stores next variables
						i++
					i++	# skips ":"
					for k in stock :
						var[stock[k]] = type[table[i]]	# registers type
					i += 2 	# skips ";"
			elif w == "while" :
				i++
				i = expression(i)
			elif w == "if" :
				i++
				i = expression(i)
			elif w == "put" :
				i++
			elif w == "get" :
				i++
			elif w == "return" :
				i++
		print(chain)
		

def program(lexical_analyser):
	specifProgPrinc(lexical_analyser)
	lexical_analyser.acceptKeyword("is")
	corpsProgPrinc(lexical_analyser)
	
def specifProgPrinc(lexical_analyser):
	lexical_analyser.acceptKeyword("procedure")
	ident = lexical_analyser.acceptIdentifier()
	logger.debug("Name of program : "+ident)
	
def  corpsProgPrinc(lexical_analyser):
	if not lexical_analyser.isKeyword("begin"):
		logger.debug("Parsing declarations")
		partieDecla(lexical_analyser)
		logger.debug("End of declarations")
	lexical_analyser.acceptKeyword("begin")

	if not lexical_analyser.isKeyword("end"):
		logger.debug("Parsing instructions")
		suiteInstr(lexical_analyser)
		logger.debug("End of instructions")
			
	lexical_analyser.acceptKeyword("end")
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
	ident = lexical_analyser.acceptIdentifier()
	logger.debug("Name of procedure : "+ident)
       
	partieFormelle(lexical_analyser)

	lexical_analyser.acceptKeyword("is")
	corpsProc(lexical_analyser)
       

def fonction(lexical_analyser):
	lexical_analyser.acceptKeyword("function")
	ident = lexical_analyser.acceptIdentifier()
	logger.debug("Name of function : "+ident)
	
	partieFormelle(lexical_analyser)

	lexical_analyser.acceptKeyword("return")
	nnpType(lexical_analyser)
        
	lexical_analyser.acceptKeyword("is")
	corpsFonct(lexical_analyser)

def corpsProc(lexical_analyser):
	if not lexical_analyser.isKeyword("begin"):
		partieDeclaProc(lexical_analyser)
	lexical_analyser.acceptKeyword("begin")
	suiteInstr(lexical_analyser)
	lexical_analyser.acceptKeyword("end")

def corpsFonct(lexical_analyser):
	if not lexical_analyser.isKeyword("begin"):
		partieDeclaProc(lexical_analyser)
	lexical_analyser.acceptKeyword("begin")
	suiteInstrNonVide(lexical_analyser)
	lexical_analyser.acceptKeyword("end")

def partieFormelle(lexical_analyser):
	lexical_analyser.acceptCharacter("(")
	if not lexical_analyser.isCharacter(")"):
		listeSpecifFormelles(lexical_analyser)
	lexical_analyser.acceptCharacter(")")

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
		logger.debug("integer type")
	elif lexical_analyser.isKeyword("boolean"):
		lexical_analyser.acceptKeyword("boolean")
		logger.debug("boolean type")                
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
	logger.debug("identifier found: "+str(ident))

	if lexical_analyser.isCharacter(","):
		lexical_analyser.acceptCharacter(",")
		listeIdent(lexical_analyser)
		
	# Breaks down a boolean expression using OR
	def expression(i):
		i = exp1(i)
		i++
		if table[i] == "or" :
			i++
			i = exp1(i)
		return i
		
	# Breaks down a boolean expression using AND
	def exp1(i):
		i = exp2(i)
		i++
		if table[i] == "and" :
			i++
			i = exp2(i)
		return i
		
	# Breaks down a boolean expression
	def exp2(i):
		i = exp3(i)
		i++
		if table[i] == "=" :
			i++
			i = exp3(i)
		elif table[i] == "/=" :
			i++
			i = exp3(i)
		elif table[i] == ">" :
			i++
			i = exp3(i)
		elif table[i] == ">=" :
			i++
			i = exp3(i)
		elif table[i] == "<" :
			i++
			i = exp3(i)
		elif table[i] == "<=" :
			i++
			i = exp3(i)
		return i
		
	# Breaks down an addition / substraction
	def exp3(i):
		i = exp4(i)
		i++
		if table[i] == "+" :
			i++
			i = exp4(i)
		elif table[i] == "-" :
			i++
			i = exp4(i)
		return i
		
	# Breaks down a multiplication / division
	def exp4(i):
		i = prim(i)
		i++
		if table[i] == "*" :
			i++
			i = prim(i)
		return i
		
	# Breaks down a primary operator
	def prim(i):
		if table[i] == "+" :
			i++
			i = elemPrim(i)
		elif table[i] == "-" :
			i++
			i = elemPrim(i)
		elif table[i] == "not" :
			i++
			i = elemPrim(i)
		return i
		
	# Translates an expression
	def elemPrim(i):
		if isinstance(table[i], (int, long)) :	# Integer
			i++
		elif table[i] == "true" :
			i++
		elif table[i] == "false" :
			i++
		elif table[i] == "(" :	# Boolean expression
			i++
			i = expression(i)
			i++
		else :	# Identifier / variable
			if table[i] in id :	# Identifier
				i++
			else :	# Variable
				i++
		return i
		
	def error(text):
		raise KeyError(text)
