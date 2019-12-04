# graph - adjacency version
import copy as cp
import glob
import os
import random as rd

def bfs(start, data):
	adj = cp.deepcopy(data)
	vertex = len(adj)
	queue = [start]
	visited[start] = True
	sequence = []
	while queue:
		now = queue.pop(0)
		for i in range(1, vertex):	
			if adj[now][i] == 0 or visited[i]:
				if not (visited[i] and adj[now][i] != 0):
					continue
			#print(now, adj[now][i], i)
			sequence.append([now, i, adj[now][i]])
			#sequence.append([now, i, 1])
			adj[now][i] = 0
			adj[i][now] = 0
			queue += [i]
			visited[i] = True
	return sequence

def seqSave(filename, labels, sequences):
	with open(filename, 'w') as wf:
		for seq in sequences:
			u, v, w = seq
			sequence = [labels[u], labels[v], w]
			wf.write(str(sequence) + "\n")

root_dir = './group/'
save_dir = './seq/'
#for idx in range(1, 7):
#dir_name = root_dir + str(idx) + "/*"
dir_name = root_dir + '/'

dirs = len(glob.glob(root_dir + '/*'))
print(dirs)

for group in range(dirs):
	all_files = glob.glob(dir_name+str(group)+'/*')
	rd.shuffle(all_files)
	for idx, file in enumerate(all_files):
		if idx == 100:
			break
		read_file = file.split('/')[-1].replace('.txt', '')
		save_name = save_dir + str(group) + '/' + read_file
		print(save_name)

		with open(file, 'r') as rf:
			lines = rf.readlines()
			node_name = lines[0][:-1].split(' ')
			print(node_name)

			data = []
			for line in lines[2:]:
				data.append(list(map(float, line[:-1].split(' '))))
	
		visited = [False for i in range(len(data))]
		for i in range(1, len(data)):
			save_filename = save_name + "-" + str(i) +".txt"
			#print(save_filename)
			seq = bfs(i, data)
			if len(seq) != 0:
				seqSave(save_filename, node_name, seq)
