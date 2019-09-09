# graph - adjacency version
import copy as cp

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
			sequence.append((now, i, adj[now][i]))
			adj[now][i] = 0
			adj[i][now] = 0
			queue += [i]
			visited[i] = True
	return sequence


file = open('graph/datasets/graph1.txt', 'r')
data = []
for r in file:
	data.append(list(map(float, r.split())))

visited = [False for i in range(len(data))]

for i in range(1, len(data)):
	print('start', i, bfs(i, data))