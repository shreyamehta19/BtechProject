	def plot_graph_methods(self, list_of_methods, method_names, outlier_method_names, remaining_method_names):
		
		plt.clf()
		out_method_values = []
		for name in outlier_method_names:
			i = method_names.index(name)
			out_method_values.append(list_of_methods[i])
		rem_method_names = []
		rem_method_values = []
		for name in method_names:
			if name not in outlier_method:
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
			label = out_method_names[i]
			i = i + 1
			plt.annotate(label, (x, y), textcoords="offset points", xytext = (0, 10), ha = "center")
			
		i = 0
		for x, y in zip(x_rem, y_rem):
			#label = "{:.2f}".format(y)
			label = rem_method_names[i]
			i = i + 1
			plt.annotate(label, (x, y), textcoords="offset points", xytext = (0, 10), ha = "center")

		plt.xticks(np.arange(0, 0.5, 0.1))
		plt.yticks(np.arange(0, 20, 2))

		plt.show()

