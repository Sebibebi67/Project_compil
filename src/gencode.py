# This class translates VALself.id pseudo code (see examples) into NilNovi Object code. It does not consself.ider grammatical errors, those must be treated before this program is run.

test = ["procedure", "pp", "is", "i", ",", "j", ",", "k", ":", "integer", ";", "begin", "if", "1","<","2","then", "get", "j", ";","end", "end"]

class Generator(object):

	s = ";\n"  # separator
	chain = "debutProg()" + s 	# NilNovi code
	lines = 1 	# line counter of the NNP code
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
				self.chain += "reserver(" + str(len(self.stock)) + ")" + self.s		# NNP : blocking addresses
				self.lines += 1
				self.stock = []
				i += 1 	# skips "begin"
				
				
			elif self.table[i] != "end":
				i, instr = self.instructions(i)
				self.chain += instr
				
				
			else :
				self.chain += "finProg()"
				self.lines += 1
				i += 2 	# skips "."
				
		print(self.chain)
		print(self.lines)



	# Breaks down an instructions block TODO
	# Ends on the line AFTER the block
	def instructions(self, i):
		total, expr, instr = "", "", ""
		
		if self.table[i] == "while":
			i += 1
			i = self.expression(i)		# condition
			i += 1		# skips "loop"
			i = self.instructions(i)	# instructions
			i += 1		# skips "end"
				
				
		elif self.table[i] == "if":
			i += 1
			i, expr = self.expression(i)	# condition
			i += 1		# skips "then"
			self.lines += 1 	# line reserved for "tze"
			i, instr = self.instructions(i)	# instructions
			expr += "tze(" + str(self.lines) + ")" + self.s 	# jumps to end if the condition is false
			expr += instr
			
			if self.table[i] == "else":
				i, instr = self.instructions(i)	# else instructions
				self.lines += 1 	# line reserved for "tra"
				expr += "tra(" + str(self.lines) + ")" + self.s 	# jumps to end if the condition is true
				expr += instr
			i += 1		# skips "end"
			total += expr
			
			
		elif self.table[i] == "put":
			i += 1
			i, expr = self.expression(i)
			total += expr
			total += "put()" + self.s
			self.lines += 1
			i += 2		# skips ";"
			
			
		elif self.table[i] == "get":
			i += 1
			total += "empilerAd(" + str(self.var[self.table[i]]) + ")" + self.s 	# NNP : stacks the variable
			total += "get()" + self.s
			self.lines += 2
			i += 2		# skips ";"
			
		
		elif self.table[i] in self.id :	# identifier
			i += 1
				
				
		elif self.table[i] in self.var : # variable assignment
			total += "empilerAd(" + str(self.var[self.table[i]]) + ")" + self.s
			self.lines += 1
			i += 2 	# skips ":="
			i, expr = self.expression(i)
			total += expr
			total += "affectation()" + self.s
			self.lines += 1
		
			
		elif self.table[i] == "return":
			i += 2
			i = self.expression(i)
			
		return i, total
		
		
		
	# Breaks down a boolean expression using OR TODO
	# Ends on the line AFTER the expression
	def expression(self, i):
		expr, e = "", ""
		i, expr = self.exp1(i)
		
		if self.table[i] == "or" :
			i += 1
			i, e = self.exp1(i)
			e += "ou()" + self.s
			self.lines += 1
			
		return i, expr+e
		
		
		
	# Breaks down a boolean expression using AND TODO
	def exp1(self, i):
		expr, e = "", ""
		i, expr = self.exp2(i)
		
		if self.table[i] == "and" :
			i += 1
			i, e = self.exp2(i)
			e += "et()" + self.s
			self.lines += 1
			
		return i, expr+e
		
		
		
	# Breaks down a boolean expression TODO
	def exp2(self, i):
		expr, e = "", ""
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
		
		
		
	# Breaks down an addition / substraction TODO
	def exp3(self, i):
		expr, e = "", ""
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
		
		
		
	# Breaks down a multiplication / division TODO
	def exp4(self, i):
		expr, e = "", ""
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
		
		
		
	# Translates a primary operator TODO
	def prim(self, i):
		expr = ""
		i, expr = self.elemPrim(i)
		
		if self.table[i] == "+" :
			i += 1
			
			
		elif self.table[i] == "-" :
			i += 1
			expr += "moins()" + self.s
			self.lines += 1
			
			
		elif self.table[i] == "not" :
			i += 1
			expr += "non()" + self.s
			self.lines += 1
			
		return i, expr
		
		
		
	# Translates an expression TODO
	def elemPrim(self, i):
		expr = ""
		
		if self.table[i].isdigit() :	# Integer
			expr += "empiler(" + str(self.table[i]) + ")" + self.s
			self.lines += 1
			i += 1
			
			
		elif self.table[i] == "true" :
			i += 1
			
			
		elif self.table[i] == "false" :
			i += 1
			
			
		elif self.table[i] == "(" :	# Boolean expression
			i += 1
			i, expr = self.expression(i)
			i += 1
			
			
		else :	# identifier / variable
		
			if self.table[i] in self.id :	# identifier
				i += 1
				
			else :	# variable
				expr += "empilerAd(" + str(self.var[self.table[i]]) + ")" + self.s
				expr += "valeurPile()" + self.s
				self.lines += 2
				i += 1
				
		return i, expr
