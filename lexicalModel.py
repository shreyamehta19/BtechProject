import configparser
import re
import threading
config = configparser.ConfigParser()

class TokenGenerator():

	UAST_text = [] 			#List of lines of the UAST
	tokens = [] 				#List of the tokens
	result = []
	data = []					#Tokens exclusive of the class names, method names, class and method declarations
	class_var = []				#Variables that are class members
	method_var = []				#Variables that are method members
	type_stack_size = 0 			#Stack Level 1=>class >2=>method
	class_bracket_count = 0
	method_bracket_count = 0
	class_name_flag = 1			#Flag set to 0 indicates class name not known yet
	method_name_flag = 1		#Flag set to 0 indicates method name not known yet
	method_info = []	
	class_name = ""
	
	def UASTReader(self, fileName):
		fp = open(fileName, "r")
		self.UAST_text = fp.readlines()
	
	
	def TokensGenerator(self):
		for line in self.UAST_text:
			self.tokens = self.tokens + line.split()
	
	
	def FunctionNameIdentifier(self, token, i):
		if(self.method_name_flag == 1  and self.tokens[i+2] == config.get('Section1', 'method_declaration')):
			self.method_name_flag = 0
			self.method_bracket_count = self.method_bracket_count + 1
			self.class_bracket_count = self.class_bracket_count + 1
			self.type_stack_size = self.type_stack_size + 1
		elif(self.method_name_flag == 0):
			method_name = self.tokens[i+18]
			self.method_name_flag = 1	
			self.method_info = [self.class_name, method_name]
	
	
	def ClassNameIdentifier(self, token, i):
		if(self.class_name_flag == 1 and self.tokens[i+2] == config.get('Section1', 'class_or_interface_declaration')):
			self.class_name_flag = 0
			self.class_bracket_count = self.class_bracket_count + 1
			self.type_stack_size = self.type_stack_size + 1
		elif(self.class_name_flag == 0):
			self.class_name_flag = 1
			self.class_name = self.tokens[i+18]

	
	def VariableAllocator(self, i):
		if(self.tokens[i+4] == "Declaration" and self.tokens[i+6] == "Identifier"):
			if(self.type_stack_size >= 2):
				if(self.tokens[i+22] is not "}"):
					self.method_var.append(self.tokens[i+22])
			elif(self.type_stack_size == 1):
				self.class_var.append(self.tokens[i+22])	
	
				
	def EndTagHandler(self):
		if(self.type_stack_size >= 2):
			self.method_bracket_count = self.method_bracket_count - 1;
			self.class_bracket_count = self.class_bracket_count - 1;
			if(self.method_bracket_count == 0):
				self.type_stack_size = self.type_stack_size-1;			
				method_data = self.method_info + self.data
				self.result = self.result + [method_data]
				self.method_info = []
				self.data = []
		if(self.type_stack_size == 1):
			self.class_bracket_count = self.class_bracket_count - 1
			if(self.class_bracket_count == 0):
				self.type_stack_size = self.type_stack_size-1;			
				self.class_name = ""


	def MethodSummarizer(self):
		for i in range(0, len(self.result)):
			method_data = self.result[i]
			if(method_data == []):
				continue
			class_name = method_data[0].replace("\"", "")
			method_name = method_data[1].replace("\"", "")
			method_head = [class_name, method_name]
			method_words = []
			for j in range(2, len(method_data)):
				token = method_data[j]
				token = token.replace("\"", "")
				if(len(token) >= 4 and ("\\" not in token) and (":" not in token ))	:
					method_words.append(token)
			print(method_head + method_words)
			print()
			print()
	
	def TokenCategoriser(self):
		config.readfp(open("config.properties"))
		tokensCount = len(self.tokens)
		for i in range(0, tokensCount):
			token = self.tokens[i]
			if(token == "{"):
				if(self.type_stack_size == 1):
					self.class_bracket_count = self.class_bracket_count+1
				if(self.type_stack_size == 2):
					self.method_bracket_count = self.method_bracket_count+1
				if(i+2 < tokensCount-1):
					if(self.tokens[i+2] == config.get('Section1', 'class_or_interface_declaration')):
						self.ClassNameIdentifier(token, i)
					elif(self.tokens[i+2] == config.get('Section1', 'method_declaration')):
						self.FunctionNameIdentifier(token, i)
				if(self.tokens[i+2] == config.get('Section1', 'simple_name')):
					self.VariableAllocator(i)
					if(self.type_stack_size >= 2):
						self.FunctionNameIdentifier(token, i)
					elif(self.type_stack_size == 1):
						self.ClassNameIdentifier(token, i)
			if(token == config.get('Section1', 'token') and self.class_name_flag == 1 and self.method_name_flag == 1 and self.type_stack_size >= 2) :
				self.data = self.data + [self.tokens[i+1]]
			if(token == "}"):
				self.EndTagHandler()

					
	def ToFileWriter(self):
		fp = open("Tokens", "w")
		for token in self.tokens:
			fp.write(token + "\n")
		fp = open("ClassDeclarations", "w")
		for var in self.class_var:
			fp.write(var + "\n")
		fp = open("MethodDeclarations","w")
		for var in self.method_var:
			fp.write(var + "\n")	
						
if(__name__ == "__main__"):
	TG = TokenGenerator()
	TG.UASTReader("Location.txt")
	TG.TokensGenerator()
	TG.TokenCategoriser()
	TG.ToFileWriter()
	TG.MethodSummarizer()							
