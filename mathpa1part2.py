from MathTree import *

class DiscreteMathAnalyzerPart2():

	def __init__(self,fileName):
		self.fileName = fileName
		self.fileContent = self.getFileContents()
		self.parsedList = self.parseList()
		
	def getFileContents(self):
		file_handle = open(self.fileName,'r')
		file_content = file_handle.readlines()
		file_handle.close()	
		return file_content
	
	def parseList(self):
		parsedList = []
		for f in self.fileContent: #go through each file
			parsedLine = []
			variables = ""
			statement = ""
			reachedStatement = 0
			
			for m in range(len(f)):  #go through each character
				#handle variables	
				if(reachedStatement == 0):
					if(f[m] == "\t"):
						reachedStatement = 1
					else:
						variables = variables +f[m]
				#handle statement
				if(reachedStatement == 1):
					statement = statement + f[m]
			
			#a bit of cleanup
			variables = variables.replace('\t','')
			variables = variables.replace(' ','')	
			statement = statement.replace('\t','')	
			statement = statement.replace('\n','')
			statement = statement.replace("TRUE","T")
			statement = statement.replace("FALSE","F")
			#add them to parsedLine
			parsedLine.append(variables)
			parsedLine.append(statement)
			#add parsedLine to parsedList
			parsedList.append(parsedLine)
			
		return parsedList

	def permutations(self, s):
		variables = s[0]
		variables = variables.split(",")
		perms = 2 ** len(variables)
		totalPerms = perms
		allPerms = []
		truth = "F"
		
		for i in range(totalPerms):
			allPerms.append([])
			while(len(allPerms[i]) < len(variables)):
				allPerms[i].append(0)

		for n in range(len(variables)): # 3 variables
			perms = (int)(perms/2)
			for i in range(totalPerms): #we have 8 perms in our example
				#first time 4 t and 4 false
				#second 2 and 2 and 2 and 2
				#third switch everytime 1,1,1,1,1,1,1,1
				if (i%perms == 0):
					if(truth == "T"):
						truth="F"
					else:
						truth="T"

				allPerms[i][n] = truth

		return allPerms

	def getAnswers(self):
		f = open("q2_out.txt","w+")
		for i in self.parsedList:
			c = self.placeTruths(i)
			answers = []
			for j in c:
				a = MathTree(j)
				a.solve()
				ans = a.answer
				answers.append(ans)
			
			a  = self.determineType(answers)
			print(a,":",answers)
			a = ""+a+"\n"
			f.write(a)

	def determineType(self, answers):
		truthCount = 0
		falseCount = 0
		type = "N/A"

		for i in answers:
			if (i == "T"):
				truthCount+=1
			if (i == "F"):
				falseCount+=1
		
		if(truthCount == 0):
			type = "CONTRADICTION"
		if(falseCount == 0):
			type = "TAUTOLOGY"
		if (falseCount !=0 and truthCount !=0):
			type = "CONTINGENCY"
		
		return type
	
	def placeTruths(self, s):
		cleanStatements = []
		statement = s
		#need to do all permutations
		allPerms = self.permutations(statement)
		
		#for statement do all permutations
		for i in range(len(allPerms)):
			#for every variable ...we want to replace it's value in statement
			truths = allPerms[i]
			statement = s[1]
			statement = statement.upper()
			
			for x in range(1,len(truths)+1):
				v = "P" + str(x)
				t = truths[x-1].upper()
				#this is our statement part in our list[varibles,truths,statement]
				statement = statement.replace(v,t)

			#to make my life easier lets put - T and - F with their appropriate one since its done first
			statement = statement.replace("- T","F")
			statement = statement.replace("- F","T")
			cleanStatements.append(statement)
		
		
		return cleanStatements	
		
	








