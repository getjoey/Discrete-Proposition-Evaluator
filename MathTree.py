class Node():
	def __init__(self, statement):
		self.statement = statement
		self.statementPermanent = statement
		self.parent = None
		self.children = []

	def setStatement(self,statement):
		self.statement = statement
	
	def addChild(self,node):
		node.parent = self
		self.children.append(node)

class MathTree():
	def __init__(self,statement):
		root = None
		self.setRoot(Node(statement))
		self.answer = "Not solved Yet"
		self.createTreeStatements()
		
	def getRoot(self):
		return self.root
	
	def setRoot(self, node):
		self.root = node

	def preOrderPrint(self,node):  #this is for adding
		if(node.statement == "T" or node.statement =="F"):
			print(node.statement,":",node.statementPermanent)
		else:
			print(node.statement)
			#print(node.statementPermanent)
		
		for n in node.children:
			self.preOrderPrint(n)

	#This is a wrapper function for the preOrderCreate so we can force always start at root
	def createTreeStatements(self):
		node = self.root
		self.preOrderCreate(node)

	def preOrderCreate(self, node):
		self.createNodeStatements(node)
		
		for n in node.children:	
			self.preOrderCreate(n)
		
	def createNodeStatements(self, node):
		s = node.statement

		while("(" in s):
			locked = False
			count = 0
			statement = ""
			for i in range(0,len(s)):
				if (s[i] == "(" and not locked ):
					locked = True
					statement = statement + s[i]
				elif(locked):
					if(s[i] == "("): #checks for repitition
						count = count + 1
						statement = statement + s[i]
					elif(s[i] == ")"):
						if (count == 0):
							statement = statement + s[i]

							#clean up...
							s = list(s)
							s[i-(len(statement)-1):i+1] = "@"
							s = "".join(s)
							s = s.replace("@","")
							while(statement[0] == " "):
								statement = statement[1:len(statement)-1]
							while(statement[0] == "("):
								statement = statement[1:len(statement)-1] #remove white space and brackets
							while (statement[0] == " "):
								statement = statement[1:len(statement) - 1]

							#add node to tree
							node.addChild(Node(statement))
							locked = False
							break
						else:
							count = count - 1
							statement = statement + s[i]
					else:
						statement = statement +s[i]

	def solve(self):
		node = self.getRoot()
		self.solve2(node) #start at root
		return self.answer

	def solve2(self, node):
		for n in node.children:
			self.solve2(n) #RECURSION POST ORDER

		value = self.calculateNode(node.statement)
		if(node != self.root):
			value = value.replace(" ","")
			node.parent.statement = node.parent.statement.replace(node.statementPermanent,value)
			node.statement = value
		else:
			if(value == "T" or value == "F"):
				self.root.statement = value
				self.answer = value
			else:
				value = self.calculateNode(self.root.statement)
				value = value.replace(" ","")
				self.root.statement = value
				self.answer = value

	def calculateNode(self,mini):
		x = "" #This is our answer holder

		#string cleanup!
		mini = mini.replace("(","")
		mini = mini.replace(")","")
		original = mini
		mini = mini.strip()
		mini = mini.split(" ")
		while("" in mini):
			for i in mini:
				if i == "":
					mini.remove(i)

		#LOGIC PART!
		if(len(mini) == 1):
			x = mini[0]
		elif(len(mini) == 2): #its a - T type statement
			if(mini[1] == "T"):
				x = "F"
			if(mini[1] == "F"):
				x = "T"
		elif(len(mini) == 3 and ("AND" in mini or "OR" in mini or "THEN" in mini or "EQ" in mini)):
			p1 = mini[0]
			mod = mini[1]
			p2 = mini[2]

			if(mod == "AND"):
				if(p1 == "T" and p2 == "T"):
					x = "T"
				else:
					x = "F"
			if(mod == "OR"):
				if(p1 == "T" or p2 == "T"):
					x = "T"
				else:
					x = "F"
				
			if(mod == "THEN"):
				if(p1 == "T" and p2 == "F"):
					x = "F"
				else:
					x = "T"
					
			if(mod == "EQ"):
				if(p1 == p2):
					x = "T"
				else:
					x = "F"
		elif(len(mini) > 3): #IT NEEDS TO BE SOLVED LEFT TO RIGHT!!!
			x = self.solveLeftToRight(original)

		return x

	def solveLeftToRight(self,s):
		#CLEAN UP STRING...
		s = list(s)
		for i in range(len(s)-1):
			if (s[i] == " " and s[i+1] == " "):
				s[i] = "@"
		s = "".join(s)
		s = s.replace("@","")

		#need to do in order of precdence, NOT, AND, OR, THEN, EQ
		while ("-" in s):
			locked = False
			miniStatement = ""
			for i in range(len(s)):
				if(locked):
					if(s[i] == "-"):
						miniStatement = "-"
					elif(s[i] == "T" or s[i] == "F"):
						miniStatement = miniStatement + s[i]
						locked = False
						x = miniStatement
						miniAnswer = self.calculateNode(x)
						s = s.replace(x,miniAnswer)
						break
					else:
						miniStatement = miniStatement + s[i]
				elif (s[i] == "-"):
					locked = True
					miniStatement = miniStatement + s[i]

		while ("AND" in s):
			locked = False
			miniStatement = ""
			for i in range(len(s)):
				if(locked):
					if(s[i] == "T" or s[i] == "F"):
						miniStatement = miniStatement + s[i]
						locked = False
						x = miniStatement
						miniAnswer = self.calculateNode(x)
						s = s.replace(x,miniAnswer)
						break
					else:
						miniStatement = miniStatement + s[i]
				elif (s[i] == "A"):
					locked = True
					miniStatement = miniStatement + s[i-2] + s[i-1]+ s[i]

		while ("OR" in s):
				locked = False
				miniStatement = ""
				for i in range(len(s)):
					if(locked):
						if(s[i] == "T" or s[i] == "F"):
								miniStatement = miniStatement + s[i]
								locked = False
								x = miniStatement
								miniAnswer = self.calculateNode(x)
								s = s.replace(x,miniAnswer)
								break;
						else:
							miniStatement = miniStatement + s[i]
					elif (s[i] == "O"):
						locked = True
						miniStatement = miniStatement + s[i-2] + s[i-1]+ s[i]	

		while ("THEN" in s):
				locked = False
				miniStatement = ""
				for i in range(len(s)):
					if(locked):
						if(s[i] == "T" or s[i] == "F"):
							miniStatement = miniStatement + s[i]
							locked = False
							x = miniStatement
							miniAnswer = self.calculateNode(x)
							s = s.replace(x,miniAnswer)
							break;
						else:
							miniStatement = miniStatement + s[i]
					elif (s[i] == "H"):
						locked = True
						miniStatement = miniStatement + s[i-3]+s[i-2] + s[i-1]+ s[i]

		while ("EQ" in s):
				locked = False
				miniStatement = ""
				for i in range(len(s)):
					if(locked):
						if(s[i] == "T" or s[i] == "F"):
							miniStatement = miniStatement + s[i]
							locked = False
							x = miniStatement
							miniAnswer = self.calculateNode(x)
							s = s.replace(x,miniAnswer)
							break;
						else:
							miniStatement = miniStatement + s[i]
					elif (s[i] == "E"):
						locked = True
						miniStatement = miniStatement + s[i-2] + s[i-1]+ s[i]		

		return s #return list