## This class translates VALID pseudo code (see examples) into NilNovi Object code. It does not consider grammatical errors, those must be treated before this program is run.

class Generator(object)
	
	s = ";\n"	# separator
	chain = "debutProg()" + s 	# NilNovi Object code
	stock = []	# temporarily stores names to allocate
	id = {}		# associates identifiers to their line number
	var = {}	# associates variables to their type
	table = []	# pseudo code
	type = {"integer" : 0,
			"boolean" : 1}
		
	# The constructor
	def __init__(self, t):
		self.table = t
	
	# Main function TODO
	def generate():
		i = 0 	# current line
		while i < len(table) :
			if table[i] == "procedure" :
				i++
				id[table[i]] = i 	# stores procedure identifier
				i++
			elif table[i] == "is" :
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
			elif table[i] == "end" :
			else :
				i = instructions(i)
		print(chain)
		
	# Breaks down an instructions block TODO
	# Ends on the line AFTER the block
	def instructions(i):
			if table[i] == "while" :
				i++
				i = expression(i)
				i++		# skips "loop"
				i = instructions(i)
				i++		# skips "end"
			elif table[i] == "if" :
				i++
				i = expression(i)
				i++		# skips "then"
				i = instructions(i)
				if table[i] == "else" :
					i = instructions(i)
				i++		# skips "end"
			elif table[i] == "put" :
				i++
				i = expression(i)
				i++		# skips ")"
			elif table[i] == "get" :
				i += 2
				i++		# skips ")"
			elif table[i] == "return" :
				i += 2
				i = expression(i)
		return i
		
	# Breaks down a boolean expression using OR TODO
	# Ends on the line AFTER the expression
	def expression(i):
		i = exp1(i)
		i++
		if table[i] == "or" :
			i++
			i = exp1(i)
		return i
		
	# Breaks down a boolean expression using AND TODO
	def exp1(i):
		i = exp2(i)
		i++
		if table[i] == "and" :
			i++
			i = exp2(i)
		return i
		
	# Breaks down a boolean expression TODO
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
		
	# Breaks down an addition / substraction TODO
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
		
	# Breaks down a multiplication / division TODO
	def exp4(i):
		i = prim(i)
		i++
		if table[i] == "*" :
			i++
			i = prim(i)
		return i
		
	# Breaks down a primary operator TODO
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
		
	# Translates an expression TODO
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
