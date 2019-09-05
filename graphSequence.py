#data = load()
'''
from collections import namedtuple
Pair = namedtuple("Pair", ["u", "v", "weight"])
'''
def bfs(graph, start):
	visited = []
	queue = [start]
	
	while queue:
		node = queue.pop(0)
		if node not in visited:
			visited.append(node)
			queue += graph[node]	
	return visited

def makePairs(parent, childs, weights):
	pairs = []
	for (child, weight) in zip(childs, weights):
		pairs.append((parent, child, weight))
	return pairs

def bfs_w(graph, weights, start):
	visited = []
	queue = [start]
	pairs = []
	while queue:
		node = queue.pop(0)
		if node not in visited:
			visited.append(node)
			next_N = [item for item in graph[node] if item not in visited]
			next_W = weights[node][len(weights[node]) - len(next_N):]
			if len(next_N) == 0:
				continue
			#print(node, next_N, next_W)
			#print(graph[node], visited, [item for item in graph[node] if item not in visited])
			pairs += makePairs(node, next_N, next_W)
			queue += next_N
	print('pair\n', pairs)
	print()
	print('node', visited)

class GraphSequence:
	if __name__ == "__main__":
	    graph = {
	        'A': ['B'],
	        'B': ['A', 'C', 'H'],
	        'C': ['B', 'D'],
	        'D': ['C', 'E', 'G'],
	        'E': ['D', 'F'],
	        'F': ['E'],
	        'G': ['C'],
	        'H': ['B', 'I', 'J', 'M'],
	        'I': ['H'],
	        'J': ['H', 'K'],
	        'K': ['J', 'L'],
	        'L': ['K'],
	        'M': ['H']
	    }

	    weight = {
	    	'A': [3],
	        'B': [3, 7, 2],
	        'C': [7, 1],
	        'D': [1, 1, 6],
	        'E': [1, 4.5],
	        'F': [4.5],
	        'G': [6],
	        'H': [2, 1.3, 2.3, 4.2],
	        'I': [1.3],
	        'J': [2.3, 3.1],
	        'K': [3.1, 2.8],
	        'L': [2.8],
	        'M': [4.2]
	    }

	    #print(bfs(graph, 'A'))
	    bfs_w(graph, weight, 'A')
    