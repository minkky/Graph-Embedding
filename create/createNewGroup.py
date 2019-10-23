import copy, random

def writeFile(filename, content):
	with open(filename, 'w') as wf:
		for c in content:
			dt = ' '.join([str(0) if i==0 else str(i) for i in c]) + '\n'
			wf.write(dt)


read_dir = 'represent/'
read_file = read_dir + 'original1.txt'
write_dir = 'group/group1/'
write_file = write_dir + '1graph'

read_data = []
with open(read_file, 'r') as rf:
	for line in rf.readlines():
		read_data.append(list(map(float, line.split(' '))))

index = [[1, 3], [1, 4], [1, 5], [6, 9], [6, 10], [6, 11], [2, 1], [2, 7], [2, 6], [2, 8]]
for i in range(100):
	R = random.randint(2, 4)
	print('#', i, ' ', R)
	filename = write_file + str(i+1) + '.txt'
	matrix = copy.deepcopy(read_data)
	for_use = []
	used = [0 for i in range(10)]
	idx = random.randint(0, 5)
	for i in range(R):
		while used[idx] == 1:
			if i % 3 == 0:
				idx = random.randint(0, 9)
			else:
				idx = random.randint(0, 5)
		used[idx] = 1
		for_use.append(index[idx])
	
	for use in for_use:
		x, y = use
		value = matrix[x][y]
		bound = matrix[x][y] * 0.2
		change = random.uniform(value - bound, value + bound)
		change = round(change, 4)
		matrix[x][y] = matrix[y][x] = change

		print(change)
	print(matrix)
	writeFile(filename, matrix)
		

	#with open(filename) as wf:

