import astclient as astclient
import glob
import sys
from datetime import datetime
import pickle 
import ast_pb2

def run():

	arguments = sys.argv[1:]
	path = arguments[0]
	client = astclient.AstClient("192.168.3.103:50051")
	filename = "uast"
	i = 1
	for filepath in glob.iglob(path+"/**/*.java", recursive=True):
		file = open(filepath, "r")
		text = file.read()
		ast = client.parse("java", text)
		f = open(path + "/"+ filename + str(i) , "w")
		dbfile = open(path + "/pickle" + str(i) , 'ab')
		f.write(str(ast))
		f.close()
		i = i + 1
		pickle.dump(ast, dbfile)                      
		dbfile.close() 
if __name__ == '__main__':
    run()
	#find_file_diff()
