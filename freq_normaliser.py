import matplotlib.pyplot as plt
import numpy as np

class freq_normaliser() :
	def __init__(self, global_list):
		self.global_list = global_list
		self.func_outlier()

	def freq_normaliser(self, list_of_all_tokens):
		token_path_distance = []
		for token in list_of_all_tokens:
			individual_token_distance = 1 / (token[1] + 0.00001)     # 0.0001 to make the denominator not equal to 0
			token_path_distance = token_path_distance + [individual_token_distance]
		return token_path_distance

	def func_outlier(self):
		all_tokens = []
		outlier_method_names = []
		path_distance_of_all_tokens = []
		sum_of_freq = 0
		count_of_freq_method = []
		count_of_norm_thresh_freq = []

		#print(self.global_list)
		for method_list in self.global_list:
			#print(method_list)
			count = 0	
			for token in method_list:
				all_tokens.append(token[0])
				sum_of_freq = sum_of_freq + token[1]
				
			normalised_dist = self.freq_normaliser(method_list)

			#print("NORMALIZED DIST")
			#print(normalised_dist)

			min_in_norm_dist = min(normalised_dist)
			max_in_norm_dist = max(normalised_dist)
			threshold_for_path_dist = (min_in_norm_dist + max_in_norm_dist) * 0.4

			#print("THRESHOLD_IN_PATH_DISTANCE:")
			#print(threshold_for_path_dist)

			for dist in normalised_dist:
				path_distance_of_all_tokens.append(dist)
				if(dist >= threshold_for_path_dist):
					count = count + 1

			count_of_freq_method.append(count)
			#print("COUNT")
			#print(count)

		for i in range(0, len(count_of_freq_method)):
			count_of_norm_thresh_freq.append(count_of_freq_method[i] / sum_of_freq)
			#print(count_of_freq_method[i] / sum_of_freq)
		
		#print("COUNT OF FREQ METHOD")
		#print(count_of_norm_thresh_freq)


		min_in_outlier = min(count_of_norm_thresh_freq)
		max_in_outlier = max(count_of_norm_thresh_freq)
		thresh_for_outlier = (min_in_outlier + max_in_outlier) * 0.6

		#print("THRESHOLD_FOR_OUTLIER")
		#print(thresh_for_outlier)
		for i in range(0, len(count_of_freq_method)):
			if(count_of_norm_thresh_freq[i] >= thresh_for_outlier):
				outlier_method_names.append(self.global_list[i][1][0])
	
		print("NAMES OF OUTLIER METHODS")
		print(outlier_method_names)
		
		#print("==============================================")
		self.graph_plot(path_distance_of_all_tokens, all_tokens)
		#print("=================")
		#print("=================")

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