# graph - adjacency version



vertex, edge = map(int, input().split(' '))

adj = [[0]*(vertex+1) for i in range(vertex+1)]
visited = [False for i in range(vertex+1)]

def bfs(start):
	queue = [start]
	visited[start] = True
	sequence = []
	while queue:
		now = queue.pop(0)
		for i in range(1, vertex+1):	
			if adj[now][i] == 0 or visited[i]:
				if not (visited[i] and adj[now][i] != 0):
					continue
			print(now, adj[now][i], i)
			sequence.append((now, i, adj[now][i]))
			adj[now][i] = 0
			adj[i][now] = 0
			queue += [i]
			visited[i] = True
	return sequence

for i in range(edge):
	u, v, w = map(float, input().split(' '))
	u = int(u)
	v = int(v)
	adj[u][v] = adj[v][u] = w

print(bfs(1))

'''
6 7
1 2 1.5
1 3 2.4
2 3 0
2 5 1
2 4 3
3 4 4.8
3 6 2.1

11 12
1 2 3.5
2 3 1.3
2 4 2.1
3 4 3
3 7 4.1
7 8 3.1 
7 11 2.7
1 5 2.4
5 6 3.5
5 9 4.5
6 10 4.1
9 10 3.1

'''