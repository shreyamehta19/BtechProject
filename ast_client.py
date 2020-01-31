import astclient as astclient
import glob
import sys
from datetime import datetime

import ast_pb2

def NameCollector(ast) :
	for j in range(0, len(ast.children) ) :
		if(ast.children[j].internalType == "SimpleName") :
			return (ast.children[j].token)

def getTokens(ast) :
	all_tokens = []
	for i in range(0, len(ast.children) ) :
		if(ast.children[i].internalType == "SimpleName") :
			all_tokens = all_tokens + [ast.children[i].token]
		if hasattr(ast.children[i], 'children'):
			all_tokens = all_tokens + getTokens(ast.children[i])
	return all_tokens
def run():

	arguments = sys.argv[1:]
	path = arguments[0]
	client = astclient.AstClient("192.168.3.103:50051")
	for filepath in glob.iglob(path+"/**/*.java", recursive=True):
		file = open(filepath, "r")
		text = file.read()
		ast = client.parse("java", text)
		
		for i in range (0, len(ast.children)) :
			if(ast.children[i].internalType == "ClassOrInterfaceDeclaration") :
				class_name = NameCollector(ast.children[i])
				
				for j in range (0, len(ast.children[i].children)) :
					tokens = []
					if(ast.children[i].children[j].internalType == "MethodDeclaration") :
						method_name = NameCollector(ast.children[i].children[j])
						
						if hasattr(ast.children[i].children[j], 'children'):
							tokens = tokens + getTokens(ast.children[i].children[j])
						
						print(class_name + " : " + method_name)
						print(tokens)
												
		
if __name__ == '__main__':
    run()
	
