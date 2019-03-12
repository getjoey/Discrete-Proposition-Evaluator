from MathTree import *

class DiscreteMathAnalyzerPart1():
	def __init__(self,fileName):
		self.fileName = fileName
		self.fileContent = self.getFileContents()
		self.parsedList = self.parseList()
		self.cleanStatements = self.placeTruths()

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
			truths = ""
			statement = ""
			reachedTruths = 0
			reachedStatement = 0

			for m in range(len(f)):  #go through each character
				#handle variables	
				if(reachedTruths == 0):
					if(f[m] == "T" or f[m] == "F"):
						reachedTruths = 1
					else:
						variables = variables +f[m]

				#handle Truth values T or F
				if(reachedTruths == 1 and reachedStatement == 0):	
					if(f[m] == "\t"):
						reachedStatement = 1	
					else:
						truths = truths + f[m]
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
			#add to parsedLine
			parsedLine.append(variables)
			parsedLine.append(truths)
			parsedLine.append(statement)
			#add parsedLine to parsedList
			parsedList.append(parsedLine)
			
		return parsedList
	
	
	def placeTruths(self):
		cleanStatements = []
		for i in self.parsedList:
			#for every variable ...we want to replace it's value in statement
			variables = i[0].split(",")
			truths = i[1].split(",")
			statement = i[2]
			statement = statement.upper()
			
			for x in range(1,len(variables)+1):
				v = "P" + str(x)
				t = truths[x-1].upper()
				#this is our statement part in our list[varibles,truths,statement]
				statement = statement.replace(v,t)	
			
			#to make my life easier lets put - T and - F to their actual values since this is done first anyways...
			statement = statement.replace("- T","F")
			statement = statement.replace("- F","T")
			cleanStatements.append(statement)

		return cleanStatements	

	def getAnswers(self):
		f = open("q1_out.txt", "w+")
		for i in self.cleanStatements:
			a = MathTree(i)
			a.solve()
			print("a",a.answer)
			f.write(a.answer+"\n")
			






			
	
	
	
	
	

		
		

