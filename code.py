from __future__ import print_function
import configparser
import re
import xlwt 
from xlwt import Workbook 
#import nltk
#from nltk.corpus import wordnet as wn
config = configparser.ConfigParser()
import string
import collections
'''from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer'''
from pprint import pprint
import logging
import grpc
import transfer_pb2
import transfer_pb2_grpc
import knn as k
import freq_normaliser as fn

class TokenWeights:
	def __init__(self, token, freq):
		self.token = token
		self.freq = freq
		
class gRPC_transfer :
	def run(self) :
		with grpc.insecure_channel('localhost:50051') as channel:
        		stub = transfer_pb2_grpc.GreeterStub(channel)
        		response = stub.SayHello(transfer_pb2.HelloRequest(name='gRPC'))
		return(response.message)	
		
class TokenGenerator(TokenWeights):

	#fileName = ""				#UAST  file
	UAST_str = ''
	UAST_text = [] 			#List of lines of the UAST
	tokens = [] 				#List of the tokens
	result = []
	data = []					#Tokens exclusive of the class names, method names, class and method declarations
	class_var = []				#Variables that are class members
	method_var = []			#Variables that are method members
	global_method_var = []		#global list of method_var of individuals
	global_class_var = []
	global_freq_of_tokens = []	#global list of frequency of tokens of every method in a class
	global_method_info = []		#global list of method heads
	global_class_names = []
	type_stack_size = 0 		#Stack Level 1=>class >2=>method
	class_bracket_count = 0
	method_bracket_count = 0
	class_name_flag = 1			#Flag set to 0 indicates class name not known yet
	method_name_flag = 1		#Flag set to 0 indicates method name not known yet
	method_info = []	
	class_name = ""
	row_index = 0				#for writing to the file
	#tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
	
	def __init__(self, UAST_str):
		self.UAST_str = UAST_str
		self.UASTReader(UAST_str)
	
	def UASTReader(self, UAST_str):
		#fp = open(fileName, "r")
		#self.UAST_text = fp.readlines()
		self.UAST_text = UAST_str.split("/n")
		self.TokensGenerator()
	
	def TokensGenerator(self):
		for line in self.UAST_text:
			self.tokens = self.tokens + line.split()
		self.TokenCategoriser()
	
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
			if(self.class_name  != self.tokens[i+18]):
				if(self.class_name != ""):				#if class is encountered for the first time then don't add the class_var lit to global list as it would be empty
					self.global_class_var.append(self.class_var)#always append the variable declarations list of the previous class when new  class is encountered
					self.class_var = []
				self.class_name = self.tokens[i+18]
				self.global_class_names.append(self.class_name) 
					
		
	
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
				self.data = []								#clear the data_buffer that stores the tokens of each method after adding it to the global result
				self.global_method_var.append(self.method_var)	#append the method_var collected for the particular method to the global list
				self.method_var = []							#clear the buffer to make a new start for the next method
		if(self.type_stack_size == 1):
			self.class_bracket_count = self.class_bracket_count - 1
			if(self.class_bracket_count == 0):
				self.type_stack_size = self.type_stack_size-1;			
				self.class_name = ""

			
	def camel_case_split(self, str): 
		words = [[str[0]]] 
		for c in str[1:]: 
			if words[-1][-1].islower() and c.isupper(): 
            			words.append(list(c)) 
			else: 
				words[-1].append(c) 
		l = [''.join(word) for word in words]
		result = []
		for each in l :
			new = each.split("_")
			result = result + new
		return result

	
	def ExcelWriter(self):
		wb = Workbook()
		tokensSheet = wb.add_sheet('sheet_1')			#Sheet1 has the frequency
		methodVarSheet = wb.add_sheet('sheet_2')		#Sheet2 has the variables of a particular method	
		classVarSheet = wb.add_sheet('sheet_3')
		camelcaseSheet = wb.add_sheet('sheet_4')
		for i in range(0, len(self.global_freq_of_tokens)):
			method_head = self.global_method_info[i]	
			token_list = self.global_freq_of_tokens[i]	  		# tokens of ith method which corresponds to ith row of the excel sheet
			tokensSheet.write(2*i, 0, method_head[0]) 		# class name
			tokensSheet.write(2*i, 1, method_head[1])  		# method name
			camelcaseSheet.write(2*i, 0, method_head[0]) 		# class name
			camelcaseSheet.write(2*i, 1, method_head[1])  		# method name
			j = 2 
			inner_token_list = []
			inner_freq_list = []
			for token in token_list:
				tokensSheet.write(2*i, j, token.token)		#2*i is for the token
				inner_token_list = inner_token_list + [token.token]
				tokensSheet.write(2*i+1, j, token.freq)		#2*i+1 is for the frequency count of the respective token
				inner_freq_list = inner_freq_list + [token.freq]
				j = j+1
			split_tokens = []
			split_token_freq = []
			a = 0
			j = 2
			for t in inner_token_list :
				t_split = self.camel_case_split(t)
				t_length = len(t_split)
				split_tokens = split_tokens + t_split				
				for k in range(0,len(t_split)) :
					split_token_freq = split_token_freq + [inner_freq_list[a]]
				a = a + 1
			final_tokens = list(set(split_tokens))
			final_freq = []
			for b in range(0, len(final_tokens)) :
				freq = 0
				for c in range(0, len(split_tokens)) :
					if(split_tokens[c] == final_tokens[b]) :
						freq = freq + split_token_freq[c]
				final_freq = final_freq + [freq]
				camelcaseSheet.write(2*i, j, final_tokens[b])		#2*i is for the token
				camelcaseSheet.write(2*i+1, j, freq)		#2*i+1 is for the frequency count of the respective token
				j = j + 1

			methodVarSheet.write(i, 0, method_head[0])
			methodVarSheet.write(i, 1, method_head[1])			
			method_var = self.global_method_var[i]
			j = 2
			for each in method_var:
				methodVarSheet.write(i, j, each)
				j = j+1
		for i in range(0, len(self.global_class_var)):
			classVarSheet.write(i, 0, self.global_class_names[i])	# name of the ith class
			class_var = self.global_class_var[i]				# all the variables 
			j = 1
			for each in class_var:
				classVarSheet.write(i, j, each) 
				j = j + 1
		wb.save("freqLoc.xls")


	def Remove(self, duplicate): 
		final_list = [] 
		for num in duplicate: 
			if num not in final_list: 
				final_list.append(num) 
		return final_list 

	
	
	def MethodSummarizer(self):
		
		for i in range(0, len(self.result)):
			method_data = self.result[i]
			if(method_data == []):
				continue
			class_name = method_data[0].replace("\"", "")
			method_name = method_data[1].replace("\"", "")
			method_head = [class_name, method_name] 			#header of the method
			self.global_method_info.append(method_head)			#add the method head to the global list
			method_words = []					  			#method-tokens with duplication
			for j in range(2, len(method_data)):
				token = method_data[j]
				token = token.replace("\"", "")
				if(len(token) >= 4 and ("\\" not in token) and (":" not in token ))	:
					method_words.append(token)
			method_tokens	= self.Remove(method_words)			 #method-tokens without duplication	
			freq_of_tokens = []				 				#list of tokens for particular method
			for token in method_tokens:						#generating the frequency of every token in the method_tokens
				freq_of_tokens.append(TokenWeights(token, method_words.count(token)))
			self.global_freq_of_tokens.append(freq_of_tokens) 	#append this list to the global list
			self.global_method_var.append(self.method_var)		#add the declarations of particular method to the global list
		self.ExcelWriter()
	
	
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
		self.global_class_var.append(self.class_var) #add the variable declartion list of the last class
		self.MethodSummarizer()

	#using wordnet, this function gets the POS tag of the 'word'
	'''def get_POS_tag(self, word) :
		syns = wn.synsets(word)
		return(set([x.pos() for x in syns]))'''		
		
	def get_knn_score(self) :
		knn = k.KNN_NLC_Classifer()
		token_gbl_list = []
		for i in range(0, len(self.global_freq_of_tokens)):
			method_head = self.global_method_info[i]	
			token_list = self.global_freq_of_tokens[i]
			t = []
			for token in token_list:
				for j in range(0, token.freq) :
					t = t + [token.token]
			token_gbl_list = token_gbl_list + [t] 		 
		return(knn.document_similarity(token_gbl_list[0], token_gbl_list[3]))
	
	def outlier_using_freq(self) :
		freq_norm = fn.freq_normaliser(self.global_freq_of_tokens)	
					
if(__name__ == "__main__"):
	logging.basicConfig()
	GRPC = gRPC_transfer()
	data = GRPC.run()
	TG = TokenGenerator(data)
	TG.outlier_using_freq()
	knn_score = TG.get_knn_score()
	print(knn_score)
					
