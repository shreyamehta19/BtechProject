import matplotlib.pyplot as plt
import numpy as np
import time
import xlwt 
from xlwt import Workbook 

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
		print("CLASS NAME:")
		print(self.global_list[0][0])
		all_tokens = []
		outlier_method_names = []
		path_distance_of_all_tokens = []
		sum_of_freq = 0
		count_of_freq_method = []
		count_of_norm_thresh_freq = []
		list_of_all_methods = []
		remaining_method_names = []
		start = time.time()

		for method_list in self.global_list:
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
				#print(dist)
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
			list_of_all_methods.append(self.global_list[i][1][0])
			if(count_of_norm_thresh_freq[i] >= thresh_for_outlier):
				outlier_method_names.append(self.global_list[i][1][0])
			else:
				remaining_method_names.append(self.global_list[i][1][0])
	
		print("NAMES OF OUTLIER METHODS:")
		print(outlier_method_names)
		end = time.time()
		
		#self.plot_graph_all_tokens(path_distance_of_all_tokens, all_tokens)
		
		self.excel_writer(list_of_all_methods, outlier_method_names)
		self.plot_graph_methods(count_of_norm_thresh_freq, list_of_all_methods, outlier_method_names, remaining_method_names)
		
		print("TIME REQUIRED FOR FINDING THE OUTLERS IN THE FILE: ", end - start, "SECONDS")

	def plot_graph_methods(self, list_of_methods, method_names, outlier_method_names, remaining_method_names):
		
		plt.clf()
		out_method_values = []
		for name in outlier_method_names:
			i = method_names.index(name)
			out_method_values.append(list_of_methods[i])
		rem_method_names = []
		rem_method_values = []
		for name in method_names:
			if name not in outlier_method_names:
				rem_method_names.append(name)
				i = method_names.index(name)
				rem_method_values.append(list_of_methods[i])

		x_out = np.array(out_method_values)
		y_out = np.arange(0, len(out_method_values))

		x_rem = np.array(rem_method_values)
		y_rem = np.arange(0, len(rem_method_values))

		plt.scatter(x_out, y_out)
		plt.scatter(x_rem, y_rem)
		i = 0
		for x, y in zip(x_out, y_out):
			#label = "{:.2f}".format(y)
			label = outlier_method_names[i]
			i = i + 1
			plt.annotate(label, (x, y), textcoords="offset points", xytext = (0, 10), ha = "center")
			
		i = 0
		for x, y in zip(x_rem, y_rem):
			#label = "{:.2f}".format(y)
			label = rem_method_names[i]
			i = i + 1
			plt.annotate(label, (x, y), textcoords="offset points", xytext = (0, 10), ha = "center")

		plt.xticks(np.arange(0, 0.5, 0.1))
		plt.yticks(np.arange(0, 10, 1))

		plt.show()

	def excel_writer(self, all_methods, outlier_methods):
		wb = Workbook()
		method_names = wb.add_sheet('sheet_1')	

		for i in range(len(all_methods)):
			method_names.write(i, 0, all_methods[i])
			if all_methods[i] in outlier_methods:
				method_names.write(i, 1, "YES")
			else:
				method_names.write(i, 1, "NO")

		wb.save("freqLoc.xls")

	