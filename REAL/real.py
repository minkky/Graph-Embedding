import numpy as np
import csv
from pysmiles import read_smiles
import networkx as nx

def writeFile(filename, content, node_labels):
	with open(filename, 'w') as wf:
		wf.write(' '.join(node_labels) + "\n\n")
		for cont in content :
			data = ' '.join([str(0) if i == 0 else str(i) for i in cont]) + "\n"
			wf.write(data)

file = open('REAL.csv', 'r', encoding='utf-8')
f = csv.reader(file)

for idx, line in enumerate(f):
	if idx ==0:
		continue
	if len(line) == 0:
		continue
	name, smiles, _, group = line[:4]

	filename = str(group) + 'REAL' + name.split('-')[1]

	print(smiles, filename, group)
	mol = read_smiles(str(smiles))
	
	labels = mol.nodes(data='element')
	node_labels = ['0']
	for label in labels:
		node_labels += [label[1]]
	matrix = nx.to_numpy_matrix(mol, weight='order').tolist()
	content = [[0 for i in range(len(matrix) + 1)]]
	for ma in matrix:
		content.append([0] + ma)
	print()
	
	with open('group/smiles'+ group + '/' + filename +'.txt', 'w') as f:
		f.write(smiles)
	writeFile('group/' + group + '/' + filename + '.txt', content, node_labels)
	
file.close()