import copy as cp
import glob, os
def check(adj):
	total = 0
	for a in adj:
		total += sum(a)
	return total

def dfs(start, adj, sequence):
	#print(adj)
	vertex = len(adj)
	visited[start] = True

	for i in range(1, vertex):
		#print("##", start, i)
		#print(check(adj))
		if check(adj) == 0:
			#print(1)
			break
		if not visited[i] and adj[start][i]:
			#print((start, i, adj[start][i]))
			sequence.append([start, i, adj[start][i]])
			adj[start][i] = adj[i][start] = 0
			dfs(i, adj, sequence)
		elif visited[i] and adj[start][i]:
			sequence.append([start, i, adj[start][i]])
			#print((start, i, adj[start][i]))
			adj[start][i] = adj[i][start] = 0
	return sequence
	#return sequence

files = sorted(glob.glob('graph/create/groupData/*'), key=os.path.getmtime)

for f in files:
	#basefile = './sequence/' + f.replace('.txt', '').split('/')[2]
	basefile = 'dfs_sequence/' + f.replace('.txt', '').split('/')[3]
	print(f)
	file = open(f, 'r')
	data = []
	for r in file:
		data.append(list(map(float, r.split())))

	for i in range(1, len(data)):
		visited = [False for i in range(len(data))]
		visited[0] = True
		#print('start', i, bfs(i, data))
		newF = open(basefile+"-"+str(i)+'.txt', 'w+')
		adj = cp.deepcopy(data)
		sequence = []
		for seq in dfs(i, cp.deepcopy(adj), sequence):
			newF.write(str(seq) + '\n')
		newF.close()
	file.close()
