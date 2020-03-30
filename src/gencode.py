

def generate(table):
	s = ";\n"
	chain = "debutProg()" + s
	stock = []
	id = {}
	var = {}
	type = {"integer" : 0,
			"character" : 1}
	i = 0
	line = 1
	while i < len(table) :
		instr = ""
		w = table[i]
		if w == "procedure" :
			i++
			id[table[i]] = line
			i++
		elif w == "is" :
			i++
			while not table[i] == "begin" :
				stock.append(table[i])
				i++
				while table[i] == "," :
					i++
					stock.append(table[i])
					i++
				i++
				for k in stock :
					var[stock[k]] = type[table[i]]
				i += 2
	print(chain)
	
def error(text):
	raise KeyError(text)

generate()