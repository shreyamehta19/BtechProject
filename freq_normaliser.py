import matplotlib.pyplot as plt
import numpy as np

class freq_normaliser() :
	def __init__(self, global_list):
		self.global_list = global_list
		self.func_outlier()

	def freq_normaliser(self, list_of_all_tokens):
		token_path_distance = []
		for token in list_of_all_tokens:
			individual_token_distance = 1 / (token.freq + 0.00001)     # 0.0001 to make the denominator not equal to 0
			token_path_distance = token_path_distance + [individual_token_distance]
		return token_path_distance

	def func_outlier(self):
		all_tokens = []
		outlier_method_names = []
		path_distance_of_all_tokens = []
		sum_of_freq = 0

		for method_list in self.global_list:
			count = 0	
			for token in method_list:
				all_tokens.append(token.token)
				sum_of_freq = sum_of_freq + token.freq
			
			normalised_dist = self.freq_normaliser(method_list)
			
			for dist in normalised_dist:
				path_distance_of_all_tokens.append(dist)

			for dist in normalised_dist:
				if(dist > 0.4):
					count = count + 1
	
		for method_list in self.global_list:
			if((count / sum_of_freq) < 0.07):
				outlier_method_names.append(method_list[0].token)
		
		print("NAMES OF OUTLIER METHODS")
		print(outlier_method_names)
		
		self.graph_plot(path_distance_of_all_tokens, all_tokens)

	def graph_plot(self, path_dist_of_tokens, all_tokens):
		colors = np.random.rand(len(all_tokens))
		fig, ax = plt.subplots()
		y_axis = []

		for num in range(0, len(all_tokens)):
			y_axis.append(num)

		ax.scatter(path_dist_of_tokens, y_axis, c = colors)
		
		for i, txt in enumerate(all_tokens):
			ax.annotate(txt, (path_dist_of_tokens[i], y_axis[i]))	
		plt.show()