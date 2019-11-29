def writeFile(filename, content, node_labels):
	with open(filename, 'w') as wf:
		wf.write(' '.join(node_labels) + "\n\n")
		for cont in content :
			data = ' '.join([str(0) if i == 0 else str(i) for i in cont]) + "\n"
			wf.write(data)

save_name = 'BZR_MD/graph'

file_header = 'BZR_DT/BZR_MD'
con_adj = [[0 for i in range(6520)] for i in range(6520)]

indicator_file = file_header + '_graph_indicator.txt'
edge_file = file_header + '_edge_attributes.txt'
adj_file = file_header + '_A.txt'
edge_label_file = file_header + '_edge_labels.txt'
node_label_file = file_header + '_node_labels.txt'
graph_label_file = file_header + '_graph_labels.txt'

adj_file = open(adj_file, 'r')
edge_file = open(edge_file, 'r')
indicator_file = open(indicator_file, 'r')
edge_label_file = open(edge_label_file, 'r')
node_label_file = open(node_label_file, 'r')
graph_label_file = open(graph_label_file, 'r')

g_labels = [0] + list(map(int, graph_label_file.readlines()))
print(g_labels)
n_labels = [0] + list(map(int, node_label_file.readlines()))

for line, edge, e_labels in zip(adj_file.readlines(), edge_file.readlines(), edge_label_file.readlines()):
	e_labels = int(e_labels)
	if e_labels != 1:
		n1, n2 = map(int, line.split(', '))
		con_adj[n1][n2] = float(edge)

adj_file.close()	
edge_file.close()
edge_label_file.close()
node_label_file.close()

counter = 1
splits = [0 for i in range(307)]
for index, indicator in enumerate(indicator_file.readlines()):
	if int(indicator) == counter:
		splits[counter - 1] = index +1
		counter += 1
splits[counter-1] = index +2

indicator_file.close()

for ct in range(306):
	#print(ct, splits[ct], splits[ct+1]-1)
	graph = [[0 for i in range(splits[ct+1] - splits[ct] + 1)] for i in range(splits[ct+1] - splits[ct] + 1)]
	r1 = 1
	for r in range(splits[ct], splits[ct+1]):
		c1 = 1
		for c in range(splits[ct], splits[ct+1]):
			graph[r1][c1] = con_adj[r][c]
			c1 += 1
		r1 += 1

	labels = list(map(str, [g_labels[ct+1]] + n_labels[splits[ct]:splits[ct+1]]))
	writeFile(save_name + str(ct+1) + '.txt', graph, labels)