# graph - adjacency version
import copy as cp
import glob
import os

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

# sort with maked time
#files = sorted(glob.glob('graph/datasets/*'), key=os.path.getmtime)
#files = sorted(glob.glob('./group1/*'))

root_dir = './BZR_MD'
save_dir = './BZR_seq'
#for idx in range(1, 7):
#dir_name = root_dir + str(idx) + "/*"
dir_name = root_dir + '/graph'

files = len(glob.glob(root_dir + '/*'))
print(files)

for index in range(1, files+1):
	file = dir_name + str(index) + '.txt'
	print(file)
	save_name = save_dir + '/graph' + str(index) 
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
	
'''
for idx in range(len(files)):
	basefile = '../datasets/last_seq/bfs/graph' + str(idx)
	file = open('../datasets/last_graph/graph' + str(idx) + ".txt", 'r')

	data = []
	for r in file:
		data.append(list(map(float, r.split())))

	visited = [False for i in range(len(data))]
	#print(f)
	for i in range(1, len(data)):
		#print('start', i, bfs(i, data))
		newF = open(basefile+"-"+str(i)+'.txt', 'w+')
		for seq in bfs(i, data):
			newF.write(str(seq) + '\n')
		newF.close()
	file.close()
'''