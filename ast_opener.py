import pickle 

# loads ast object and returns it
def ast_returner(filename) :
	infile = open(filename,'rb')
	ast = pickle.load(infile)
	infile.close()
	return ast
