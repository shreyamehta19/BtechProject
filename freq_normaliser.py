import matplotlib.pyplot as plt
class freq_normaliser() :

	def __init__(self, global_list) :
		self.global_list = global_list
		self.func_seperator()

	def freq_normaliser(self, token_list) :
		token_distances = []
		for token in token_list :
			token_distance = 1/(token.freq + 0.00001)     #0.0001 to make the denominator not equal to 0
			token_distances = token_distances + [token_distance]
		return token_distances

	def func_seperator(self) :
		for i in range(0, len(self.global_list)) :
			token_list = self.global_list[i]
			tokens = []
			for j in range(0, len(token_list)) :
				tokens = tokens + [token_list[j].token]
			token_dist = self.freq_normaliser(token_list)
			self.graph_plot(token_dist, tokens)

	def graph_plot(self, token_dist, tokens) :
		print('hi')
		fig, ax = plt.subplots()
		y = []
		for i in range(0, len(tokens)) :
			y = y + [0]
		ax.scatter(token_dist, y)
		for i, txt in enumerate(tokens):
    			ax.annotate(txt, (token_dist[i], y[i]))
		plt.show()
		
