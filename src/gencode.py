## This function translates *valid* pseudo code (see examples) into NilNovi Object code. It does not consider grammatical errors, those must be treated before this code is run.


def generate(table):
	s = ";\n"	# separator
	chain = "debutProg()" + s
	stock = []	# temporarily stores names to allocate
	id = {}		# associates identifiers to their line number
	var = {}	# associates variables to their type
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
		elif w == "if" :
		elif w == "put" :
		elif w == "get" :
		elif w == "return" :
	print(chain)
	
def error(text):
	raise KeyError(text)

generate()