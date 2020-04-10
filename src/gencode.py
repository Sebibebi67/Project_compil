# This class translates VALID pseudo code (see examples) into NilNovi Object code. It does not consider grammatical errors, those must be treated before this program is run.


class Generator(object):

	s = ";\n"  # separator
	chain = "debutProg()" + s 	# NilNovi Object code
	stock = []  # temporarily stores names to allocate
	id = {}		# associates identifiers to their line number
	var = {}  # associates variables to their type
	table = []  # pseudo code
	type = {"integer": 0,
			"boolean": 1}

	# The constructor
	def __init__(self, t):
		self.table = t

	# Main function TODO
	def generate():
		i = 0 	# current line
		while i < len(table):
			if table[i] == "procedure":
				i += 1
				id[table[i]] = i 	# stores procedure identifier
				i += 1
			elif table[i] == "is":
				i += 1
				while not table[i] == "begin":  # declarations
					stock.append(table[i])  # stores first variable
					i += 1
					while table[i] == ",":  # there are several variables of the same type
						i += 1
						stock.append(table[i])  # stores next variables
						i += 1
					i += 1  # skips ":"
					for k in stock:
						var[stock[k]] = type[table[i]]  # registers type
					i += 2 	# skips ";"
			elif table[i] != "end":
				i = instructions(i)
		print(chain)

	# Breaks down an instructions block TODO
	# Ends on the line AFTER the block
	def instructions(i):
			if table[i] == "while":
				i += 1
				i = expression(i)
				i += 1		# skips "loop"
				i = instructions(i)
				i += 1		# skips "end"
			elif table[i] == "if":
				i += 1
				i = expression(i)
				i += 1		# skips "then"
				i = instructions(i)
				if table[i] == "else":
					i = instructions(i)
				i += 1		# skips "end"
			elif table[i] == "put":
				i += 1
				i = expression(i)
				i += 1		# skips ")"
			elif table[i] == "get":
				i += 2
				i += 1		# skips ")"
			elif table[i] == "return":
				i += 2
				i = expression(i)
			return i
		
	# Breaks down a boolean expression using OR TODO
	# Ends on the line AFTER the expression
	def expression(i):
		i = exp1(i)
		i+= 1
		if table[i] == "or" :
			i+= 1
			i = exp1(i)
		return i
		
	# Breaks down a boolean expression using AND TODO
	def exp1(i):
		i = exp2(i)
		i+= 1
		if table[i] == "and" :
			i+= 1
			i = exp2(i)
		return i
		
	# Breaks down a boolean expression TODO
	def exp2(i):
		i = exp3(i)
		i+= 1
		if table[i] == "=" :
			i+= 1
			i = exp3(i)
		elif table[i] == "/=" :
			i+= 1
			i = exp3(i)
		elif table[i] == ">" :
			i+= 1
			i = exp3(i)
		elif table[i] == ">=" :
			i+= 1
			i = exp3(i)
		elif table[i] == "<" :
			i+= 1
			i = exp3(i)
		elif table[i] == "<=" :
			i+= 1
			i = exp3(i)
		return i
		
	# Breaks down an addition / substraction TODO
	def exp3(i):
		i = exp4(i)
		i+= 1
		if table[i] == "+" :
			i+= 1
			i = exp4(i)
		elif table[i] == "-" :
			i+= 1
			i = exp4(i)
		return i
		
	# Breaks down a multiplication / division TODO
	def exp4(i):
		i = prim(i)
		i+= 1
		if table[i] == "*" :
			i+= 1
			i = prim(i)
		return i
		
	# Breaks down a primary operator TODO
	def prim(i):
		if table[i] == "+" :
			i+= 1
			i = elemPrim(i)
		elif table[i] == "-" :
			i+= 1
			i = elemPrim(i)
		elif table[i] == "not" :
			i+= 1
			i = elemPrim(i)
		return i
		
	# Translates an expression TODO
	def elemPrim(i):
		if isinstance(table[i], (int, long)) :	# Integer
			i+= 1
		elif table[i] == "true" :
			i+= 1
		elif table[i] == "false" :
			i+= 1
		elif table[i] == "(" :	# Boolean expression
			i+= 1
			i = expression(i)
			i+= 1
		else :	# Identifier / variable
			if table[i] in id :	# Identifier
				i+= 1
			else :	# Variable
				i+= 1
		return i
		
	def error(text):
		raise KeyError(text)
