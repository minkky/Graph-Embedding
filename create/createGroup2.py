import copy, random
import string

def writeFile(filename, content, use_alpha):
	with open(filename, 'w') as wf:
		wf.write(' '.join(use_alpha) + "\n\n")
		for c in content:
			dt = ' '.join([str(0) if i==0 else str(i) for i in c]) + '\n'
			wf.write(dt)

def delNodes(del_indexes):
	for delete in del_indexes:
		x, y = delete
		matrix[x][y] = matrix[y][x] = 0

def getChangeIndex(now, R, total_cnt, del_indexes):
	delNodes(del_indexes)
	for_use = []
	used = [0 for i in range(total_cnt)]
	idx = random.randint(0, 5)
	for i in range(R):
		right = 5
		while used[idx] != 0 or weight_index[idx] in del_indexes:
			idx = random.randint(0, right)
		used[idx] = 1
		for_use += [weight_index[idx]]
	return for_use

def changeAndSaveMatrix(for_use, matrix):
	for use in for_use:
		x, y = use
		value = matrix[x][y]
		change = random.uniform(value * 0.9, value * 1.1)
		change = round(change, 4)
		matrix[x][y] = matrix[y][x] = change
		#print(x, y, change)
	writeFile(filename, matrix, use_alpha)

def getModiOrDelIndexes():
	right = 5
	idx = random.randint(0, right)
	idx1 = random.randint(0, right)
	while idx == idx1:
		idx = random.randint(0, right)
	return idx, idx1

def getUseAlphaWith(mode, length):
	use_alpha = upper_case[:length]
	R = random.choice([1, 1, 1, 2])
	if mode == 2 or mode == 6:
		idx, idx1 = getModiOrDelIndexes()
		for r in range(R):
			use_alpha[modify_index[idx]] = list(string.ascii_uppercase)[random.randint(1, 24)]
			idx = idx1
	if mode == 4 or mode == 8:
		alpha = list(string.ascii_uppercase)[random.randint(1, 24)]
		use_alpha += [alpha]
	return use_alpha

def getDelIndex():
	R = random.choice([1, 1, 1, 2])
	idx, idx1 = getModiOrDelIndexes()
	indexes = []
	for r in range(R):
		indexes.append(del_weight[idx])
		idx = idx1
	return indexes

def getAddWeights(idx):
	if idx == 1 or idx == 3 or idx == 4 or idx == 6 or idx == 8 or idx == 9:
		value = max(matrix[idx]) - min(matrix[idx])
	elif idx == 2:
		value = matrix[1][2]
	elif idx == 5:
		value = matrix[3][5]
	elif idx == 7:
		value = matrix[4][7]
	elif idx == 10:
		value = matrix[6][10]
	elif idx == 11:
		value = matrix[8][11]
	elif idx == 12:
		value = matrix[9][12]
	weights = round(random.uniform(value * 0.8, value * 1.2), 4)
	return weights

def addPaddingAt(idx, weights, matrix):
	for m in matrix:
		m += [0.0]
	matrix.append([0.0 for i in range(len(matrix)+1)])
	matrix[idx][len(matrix)-1] = matrix[len(matrix)-1][idx] = weights
	return matrix

weight_index = [[1, 2], [3, 5], [4, 7], [6, 10], [8, 11], [9, 12], [1, 3], [1, 4], [3, 6], [4, 8], [6, 9], [8, 9]]
modify_index = [2, 5, 7, 10, 11, 12] #[2, 5, 7, 10, 11, 12, 1, 3, 4, 6, 8, 9]
del_index = [2, 5, 7, 10, 11, 12]
del_weight = [[1, 2], [3, 5], [4, 7], [6, 10], [8, 11], [9, 12]]
add_index = [2, 5, 7, 10, 11, 12, 1, 3, 4, 6, 8, 9]
total_cnt = len(weight_index)

upper_case = ['0'] + list(string.ascii_uppercase)
read_dir = 'represent/'
read_file = read_dir + 'original4.txt'
read_data = []
with open(read_file, 'r') as rf:
	for line in rf.readlines():
		read_data.append(list(map(float, line.split(' '))))

cnt = 13
for mode in range(5, 9): #4
	write_dir = 'group1/group' + str(cnt) + '/' + str(cnt)
	cnt += 1
	write_file = write_dir + 'graph'
	print("**mode**")
	for i in range(30):
		use_alpha = getUseAlphaWith(mode, len(read_data))
		#print('alpha', use_alpha)
		R = random.randint(2, 4)
		filename = write_file + str(i+1) + '.txt'
		if mode == 3 or mode == 7:
			del_indexes = getDelIndex()
		else:
			del_indexes = []
		matrix = copy.deepcopy(read_data)
		if mode == 4 or mode == 8:
			if i % 2 == 0:
				idx = random.choice(add_index)
			else:
				idx = random.choice(add_index[:6])
			
			weights = getAddWeights(idx)
			#print(idx, weights)
			matrix = addPaddingAt(idx, weights, matrix)
		#print(del_indexes, "*****")
		for_use = getChangeIndex(i, R, total_cnt, del_indexes)
		changeAndSaveMatrix(for_use, matrix)
