from __future__ import print_function
import configparser
import re
import xlwt 
from xlwt import Workbook 
config = configparser.ConfigParser()
import string
import collections
from pprint import pprint
import logging
import grpc
import knn as k
import freq_normaliser as fn
import astclient as astclient
import glob
import sys
from datetime import datetime
import ast_pb2
import ast_opener as ast_opener


class Preprocessing () :

	def __init__(self, global_list) :
		self.global_list = global_list		

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

	def Remove(self, duplicate): 
		unique_list = [] 
		for num in duplicate: 
			if num not in unique_list: 
				unique_list.append(num) 
		return unique_list
	
	def freq_calculator(self, method_list) :
		final_list = []
		n = len(method_list)
		visited = [False for i in range(n)]
		for i in range(n): 
			count = 0
			if (visited[i] == True): 
            			continue
			count = 1
			for j in range(i + 1, n, 1): 
				if (method_list[i] == method_list[j]): 
					visited[j] = True
					count += 1
			final_list = final_list + [[method_list[i], count]]
		return final_list
				

	def compute(self) :
		global_list = self.global_list
		#print(global_list)
		final_list_without_split = []
		final_list_with_split = []
		for sub_list in global_list :
			dict_l = self.freq_calculator(sub_list)
			final_list_without_split = final_list_without_split + [dict_l]
			#print(dict_l)
			split_tokens = []
			for t in sub_list :
				t_split = self.camel_case_split(t)
				t_length = len(t_split)
				split_tokens = split_tokens + t_split
			dict_t = self.freq_calculator(split_tokens)
			final_list_with_split = final_list_with_split + [dict_t]
			#print(dict_t)
		return final_list_with_split, final_list_without_split


class UAST_parser() :

	def NameCollector(self, ast) :
		for j in range(0, len(ast.children) ) :
			if(ast.children[j].internalType == "SimpleName") :
				return (ast.children[j].token)

	def getTokens(self, ast) :
		all_tokens = []
		for i in range(0, len(ast.children) ) :
			if(ast.children[i].internalType == "SimpleName") :
				all_tokens = all_tokens + [ast.children[i].token]
			if hasattr(ast.children[i], 'children'):
				all_tokens = all_tokens + self.getTokens(ast.children[i])
		return all_tokens

	def __init__(self):
		arguments = sys.argv[1:]
		path = arguments[0]
		#client = astclient.AstClient("192.168.3.103:50051")
		#for filepath in glob.iglob(path+"/**/*.java", recursive=True):
		for filepath in glob.iglob(path+"/**/*", recursive=True):
			#file = open(filepath, "r")
			#text = file.read()
			#ast = client.parse("java", text)
			ast = ast_opener.ast_returner(filepath)
			global_list = self.parser(ast)
			PP = Preprocessing(global_list)
			withSplit , withoutSplit = PP.compute()
			#OF1 = Outlier_Finder(withSplit)
			##OF2 = Outlier_Finder(withoutSplit)
			#OF1.outlier_using_freq()
			##OF2.outlier_using_freq()
			KNN = Outlier_Finder(global_list)
			methods = KNN.knn_matrix_generator()

	def parser(self, ast) :
		global_list = []
		for i in range (0, len(ast.children)) :
			if(ast.children[i].internalType == "ClassOrInterfaceDeclaration") :
				class_name = self.NameCollector(ast.children[i])
				
				for j in range (0, len(ast.children[i].children)) :
					tokens = []
					if(ast.children[i].children[j].internalType == "MethodDeclaration") :
						method_name = self.NameCollector(ast.children[i].children[j])
						
						if hasattr(ast.children[i].children[j], 'children'):
							tokens = tokens + self.getTokens(ast.children[i].children[j])
			
						global_list = global_list + [ [class_name] + [method_name] + tokens]
		return global_list
		

class Outlier_Finder () :

	def __init__(self, method_tokens) :
		self.method_tokens = method_tokens
	
	def outlier_using_freq(self) :
		freq_norm = fn.freq_normaliser(self.method_tokens)

	def knn_matrix_generator(self) :
		methods = k.KNN_NLC_Classifer(self.method_tokens)
		return methods


if(__name__ == "__main__"):
	logging.basicConfig()
	UAST = UAST_parser()
	#global_list = UAST.run()
	#PP = Preprosessing(global_list)
	
