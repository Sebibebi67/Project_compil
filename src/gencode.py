# This class translates VALself.id pseudo code (see examples) into NilNovi Object code. It does not consself.ider grammatical errors, those must be treated before this program is run.

test = ["procedure", "pp", "is", "i", ",", "j", ",", "k", ":", "integer", ";", "begin", "get", "j", ";", "end"]

class Generator(object):

	s = ";\n"  # separator
	chain = "debutProg()" + s 	# NilNovi Object code
	lines = 1 	# line counter of the NNO code
	stock = []  # temporarily stores names to allocate
	id = {}		# associates identifiers to their line number
	var = {}  	# associates variables to their address
	table = []  # pseudo code

	# The constructor
	def __init__(self, t):
		self.table = t
		self.generate()

	# Main function TODO
	def generate(self):
		i = 0 	# current line
		
		while i < len(self.table):
			if self.table[i] == "procedure":
				i += 1
				self.id[self.table[i]] = i 	# stores procedure identifier
				i += 1
				
				
			elif self.table[i] == "is":
				i += 1
				
				while not self.table[i] == "begin":  # declarations
					self.stock.append(self.table[i])  # stores first variable
					i += 1
					
					while self.table[i] == ",":	# there are several variables of the same type
						i += 1
						self.stock.append(self.table[i])	# stores next variable
						i += 1
					i += 3 	# skips ": [type] ;"
					
				for k in range(len(self.stock)):
					self.var[self.stock[k]] = k 	# registers each variable's address
				self.chain += "reserver(" + str(len(self.stock)) + ")" + self.s		# NNO : blocking addresses
				self.lines += 1
				self.stock = []
				i += 1 	# skips "begin"
				
				
			elif self.table[i] != "end":
				i = self.instructions(i)
				
				
			else :
				self.chain += "finProg()"
				self.lines += 1
				i += 2 	# skips "."
				
		print(self.chain)
		print(self.lines)



	# Breaks down an instructions block TODO
	# Ends on the line AFTER the block
	def instructions(self, i):
			if self.table[i] == "while":
				i += 1
				i = self.expression(i)
				i += 1		# skips "loop"
				i = self.instructions(i)
				i += 1		# skips "end"
				
				
			elif self.table[i] == "if":
				i += 1
				i = self.expression(i)
				i += 1		# skips "then"
				i = self.instructions(i)
				
				if self.table[i] == "else":
					i = self.instructions(i)
				i += 1		# skips "end"
				
				
			elif self.table[i] == "put":
				i += 1
				i = self.expression(i)
				self.chain += "put()" + self.s
				self.lines += 1
				i += 2		# skips ";"
				
				
			elif self.table[i] == "get":
				i += 1
				self.chain += "empilerAd(" + str(self.var[self.table[i]]) + ")" + self.s 	# NNO : stacks the variable
				self.chain += "get()" + self.s
				self.lines += 2
				i += 2		# skips ";"
				
				
			elif self.table[i] == "return":
				i += 2
				i = self.expression(i)
				
			return i
		
		
		
	# Breaks down a boolean expression using OR TODO
	# Ends on the line AFTER the expression
	def expression(self, i):
		i = self.exp1(i)
		
		if self.table[i] == "or" :
			i += 1
			i = self.exp1(i)
			
		return i
		
		
		
	# Breaks down a boolean expression using AND TODO
	def exp1(self, i):
		i = self.exp2(i)
		
		if self.table[i] == "and" :
			i += 1
			i = self.exp2(i)
			
		return i
		
		
		
	# Breaks down a boolean expression TODO
	def exp2(self, i):
		i = self.exp3(i)
		
		if self.table[i] == "=" :
			i += 1
			i = self.exp3(i)
			
			
		elif self.table[i] == "/=" :
			i += 1
			i = self.exp3(i)
			
			
		elif self.table[i] == ">" :
			i += 1
			i = self.exp3(i)
			
			
		elif self.table[i] == ">=" :
			i += 1
			i = self.exp3(i)
			
			
		elif self.table[i] == "<" :
			i += 1
			i = self.exp3(i)
			
			
		elif self.table[i] == "<=" :
			i += 1
			i = self.exp3(i)
			
		return i
		
		
		
	# Breaks down an addition / substraction TODO
	def exp3(self, i):
		i = self.exp4(i)
		
		if self.table[i] == "+" :
			i += 1
			i = self.exp4(i)
			
			
		elif self.table[i] == "-" :
			i += 1
			i = self.exp4(i)
			
		return i
		
		
		
	# Breaks down a multiplication / division TODO
	def exp4(self, i):
		i = self.prim(i)
		
		if self.table[i] == "*" :
			i += 1
			i = self.prim(i)
			
		return i
		
		
		
	# Breaks down a primary operator TODO
	def prim(self, i):
		
		if self.table[i] == "+" :
			i += 1
			i = self.elemPrim(i)
			
			
		elif self.table[i] == "-" :
			i += 1
			i = self.elemPrim(i)
			
			
		elif self.table[i] == "not" :
			i += 1
			i = self.elemPrim(i)
			
		else :
			i = self.elemPrim(i)
			
		return i
		
		
		
	# Translates an expression TODO
	def elemPrim(self, i):
		if isinstance(self.table[i], (int, long)) :	# Integer
			i += 1
			
			
		elif self.table[i] == "true" :
			i += 1
			
			
		elif self.table[i] == "false" :
			i += 1
			
			
		elif self.table[i] == "(" :	# Boolean expression
			i += 1
			i = self.expression(i)
			i += 1
			
			
		else :	# identifier / variable
		
			if self.table[i] in self.id :	# identifier
				i += 1
				
			else :	# variable
				i += 1
				
		return i
