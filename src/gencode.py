# This class translates VALID pseudo code (see examples) into NilNovi code. It does not consider grammatical errors, those must be treated before this program is run.

test = ['procedure', 'pp', 'is', 'procedure', 'affiche', 'is', 'i', 'j',':', 'integer', 'begin', 'i', '1', 'while', 'i', '/=', '5', 'j', '1', 'while', 'j', '/=', '5', 'put', '(', 'j', ')', 'j', 'j', '+', '1', 'end', 'i', 'i', '+', '1', 'end', 'end', 'a', 'b', 'c',':', 'integer', 'begin','get', '(', 'a', ')', 'affiche','(',')', 'b', 'a', '+', '1', 'put', '(', 'b', ')', 'end']

class Generator(object):

	s = ";\n" 	# separator
	lines = 1 	# line counter of the NNP code
	id = {}		# associates identifiers to their line numbers
	var = {}  	# associates variables to their addresses
	param = {} 	# associates parameters to their local adresses
	table = []  # pseudo code

	# The constructor
	def __init__(self, t):
		self.table = t
		_, chain = self.generate(0, "debutProg()" + self.s)
		self.printNoLines(chain)

	# Main function TODO
	def generate(self, i, chain):
		stock = []  # temporarily stores names to allocate
		
		while i < len(self.table):
			if self.table[i] == "procedure" or self.table[i] == "function" :
				if self.table[i] == "procedure" :
					proc = True
				else :
					proc = False
				i += 1
				self.id[self.table[i]] = self.lines 	# stores procedure / function identifier
				i += 1
				
				if self.table[i] == "(" : 	# parameters
					
					while not self.table[i] != ")" :
						stock.append(self.table[i])  # stores first parameter
						i += 4 	# skips ": [in/out] [type]"
						
					for k in range(len(stock)):
						self.param[stock[k]] = k 	# registers each parameter's number
					stock = []
				
				
			elif self.table[i] == "is":
				i += 1
				
				if self.table[i] == "procedure" or self.table[i] == "function" :
					self.lines += 1 	# line reserved for "tra"
					i, temp = self.generate(i, "")
					chain += "tra(" + str(self.lines+1) + ")" + self.s
					chain += temp
				
				while self.table[i] != "begin":  # declarations
					stock.append(self.table[i])  # stores first variable
					i += 1
					
					if self.table[i] == ":" :
						i += 2 	# skips ": [type]"
					
				for k in range(len(stock)):
					self.var[stock[k]] = k 	# registers each variable's address
				chain += "reserver(" + str(len(stock)) + ")" + self.s
				self.lines += 1
				stock = []
				i += 1 	# skips "begin"
				
				
			elif self.table[i] != "end":
				i, instr = self.instructions(i)
				chain += instr
			
			
			else :
				if proc :
					chain += "retourProc()" + self.s
				self.param = {}
				self.var = {}
				i += 1
				if i == len(self.table) :	# program ends
					chain += "finProg()"
					self.lines += 1
				break 	# end of procedure / function
				
		return i, chain



	# Breaks down an instructions block TODO
	# Ends on the line AFTER the block
	def instructions(self, i):
		total, expr, instr = "", "", "" 	# used for "tze" / "tra" insertion
		
		if self.table[i] == "while":
			i += 1
			lines = self.lines 	# first line of condition
			i, expr = self.expression(i)	# condition
			self.lines += 1 	# line reserved for "tze"
			while self.table[i] != "end" :
				i, block = self.instructions(i) # instructions
				instr += block
			expr += "tze(" + str(self.lines+1) + ")" + self.s 	# jumps to end if the condition is false
			expr += instr
			expr += "tra(" + str(lines) + ")" + self.s 	# loops to condition
			self.lines += 1
			i += 1		# skips "end"
			total += expr
				
				
		elif self.table[i] == "if":
			i += 1
			i, expr = self.expression(i)	# condition
			self.lines += 1 	# line reserved for "tze"
			while self.table[i] != "end" and self.table[i] != "else" :
				i, block = self.instructions(i) # instructions
				instr += block
			expr += "tze(" + str(self.lines) + ")" + self.s 	# jumps to end if the condition is false
			expr += instr
			instr = ""
			
			if self.table[i] == "else":
				self.lines += 1 	# line reserved for "tra"
				while self.table[i] != "end" and self.table[i] != "else" :
					i, block = self.instructions(i) # else instructions
					instr += block
				expr += "tra(" + str(self.lines) + ")" + self.s 	# jumps to end if the condition is true
				expr += instr
			i += 1		# skips "end"
			total += expr
			
			
		elif self.table[i] == "put":
			i += 2 	# skips "("
			i, expr = self.expression(i)
			total += expr
			total += "put()" + self.s
			self.lines += 1
			i += 1 	# skips ")"
			
			
		elif self.table[i] == "get":
			i += 2 	# skips "("
			total += "empilerAd(" + str(self.var[self.table[i]]) + ")" + self.s
			total += "get()" + self.s
			self.lines += 2
			i += 2 	# skips ")"
			
		
		elif self.table[i] in self.id :	# call to identifier
			call = self.id[self.table[i]]
			paramCount = 0
			total += "reserverBloc()" + self.s
			self.lines += 1
			i += 2 	# skips "("
			
			while self.table[i] != ")" :
				i, expr = self.expression(i)
				total += expr
				paramCount += 1
				i += 1
			i += 1 	# skips ")"
			
			total += "traStat(" + str(call) + "," + str(paramCount) + ")" + self.s
			self.lines += 1
				
				
		elif self.table[i] in self.var : # variable assignment
			total += "empilerAd(" + str(self.var[self.table[i]]) + ")" + self.s
			self.lines += 1
			i += 1
			i, expr = self.expression(i)
			total += expr
			total += "affectation()" + self.s
			self.lines += 1
				
				
		elif self.table[i] in self.param : # parameter assignment
			total += "empilerParam(" + str(self.param[self.table[i]]) + ")" + self.s
			self.lines += 1
			i += 1
			i, expr = self.expression(i)
			total += expr
			total += "affectation()" + self.s
			self.lines += 1
		
			
		elif self.table[i] == "return":
			i += 1
			i, expr = self.expression(i)
			total += expr
			total += "retourFonct()" + self.s
			self.lines += 1
			
		return i, total
		
		
		
	# Breaks down a boolean expression using OR
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
		
		
		
	# Breaks down a boolean expression using AND
	# Ends on the line AFTER the expression
	def exp1(self, i):
		expr, e = "", ""
		i, expr = self.exp2(i)
		
		if self.table[i] == "and" :
			i += 1
			i, e = self.exp2(i)
			e += "et()" + self.s
			self.lines += 1
			
		return i, expr+e
		
		
		
	# Breaks down a boolean expression
	# Ends on the line AFTER the expression
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
		
		
		
	# Breaks down an addition / substraction
	# Ends on the line AFTER the expression
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
		
		
		
	# Breaks down a multiplication / division
	# Ends on the line AFTER the expression
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
		
		
		
	# Translates a primary operator
	# Ends on the line AFTER the expression
	def prim(self, i):
		
		if self.table[i] == "+" :
			i += 1
			i, expr = self.elemPrim(i)
			
		
		if self.table[i] == "-" :
			i += 1
			i, expr = self.elemPrim(i)
			expr += "moins()" + self.s
			self.lines += 1
			
			
		elif self.table[i] == "not" :
			i += 1
			i, expr = self.elemPrim(i)
			expr += "non()" + self.s
			self.lines += 1
			
		else :
			i, expr = self.elemPrim(i)
			
		return i, expr
		
		
		
	# Translates an expression TODO
	# Ends on the line AFTER the expression
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
			i += 1 	# skips ")"
			
			
		else :	# identifier / variable / parameter
		
			if self.table[i] in self.id :	# identifier
				i += 1
				
			elif self.table[i] in self.var :	# variable
				expr += "empilerAd(" + str(self.var[self.table[i]]) + ")" + self.s
				expr += "valeurPile()" + self.s
				self.lines += 2
				i += 1
				
			else : 	# parameter
				expr += "empilerParam(" + str(self.var[self.table[i]]) + ")" + self.s
				expr += "valeurPile()" + self.s
				self.lines += 2
				i += 1
				
		return i, expr
		
		
		
	def printNoLines(self, chain):
		table = chain.split(";\n")
		for l in range(self.lines):
			print(table[l])
		
		
		
	def printWithLines(self, chain):
		table = chain.split(";\n")
		space = "  "
		for l in range(self.lines):
			if l > 9 : space = " "
			print(str(l) + space + table[l])
