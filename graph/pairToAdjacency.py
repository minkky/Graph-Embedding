import sys

def saveMatrix(data, name):
	filename = './datasets/graph' + name + '.txt'
	f = open(filename, 'w+')

	for i in data:
		for j in i:
			f.write(str(j) + " ")
		f.write("\n")
	f.close()

N = sys.argv[1]
file = open('gg_' + N+ 'x' + N + '.al', 'r')
N = int(N)
data = [[0 for i in range(N+1)] for i in range(N+1)]
#print(data)
for r in file:
	r = r.replace('\n', '')
	print(r.split(' ')[:3])
	(i, j, k) = r.split(' ')[:3]
	if data[int(i)][int(j)] != 0:
		continue
	data[int(i)][int(j)] = float(k)
	data[int(j)][int(i)] = float(k)

file.close()

saveMatrix(data, sys.argv[2])