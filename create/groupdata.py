import copy, random, string

def writeFile(filename, content, use_alpha):
	with open(filename, 'w') as wf:
		wf.write(' '.join(use_alpha) + "\n\n")
		for cont in content :
			data = ' '.join([str(0) if i == 0 else str(i) for i in cont]) + "\n"
			wf.write(data)

def getModiOrDelIndexes(count):
	if case == 1:
		if count % 2 == 0:
			right = 7
		else:
			right = 5
	elif case == 2:
		right = 5
	elif case == 3:
		right = 3
	idx = random.randint(0, right)
	idx1 = random.randint(0, right)
	while idx == idx1:
		idx = random.randint(0, right)
	return idx, idx1

def getUseAlphaWith(index, use_alpha, modify_R):
	idx, idx1 = getModiOrDelIndexes(index)
	print(idx, 'idx, idx1, modiR ', idx, idx1, modify_R)
	for r in range(modify_R):
		use_alpha[modify_index[idx]] = list(string.ascii_uppercase)[random.randint(1, 24)]
		idx = idx1
	return use_alpha

def getR():
	if case == 3:
		arr = [0, 0, 0, 1, 1, 1]
	else:
		arr = [0, 0, 0, 0, 1, 1, 1, 2]
	random.shuffle(arr)
	return random.choice(arr)

def getDelIndex(count):
	idx, idx1 = getModiOrDelIndexes(count)
	indexes = []
	for r in range(count):
		indexes.append(del_weight[idx])
		idx = idx1
	return indexes

def getAddWeights(idx):
	if case == 1:
		if idx == 1:
			value = max(matrix[1]) - min(matrix[1])
		elif idx == 3:
			value = matrix[1][3]
		elif idx == 4:
			value = matrix[1][4]
		elif idx == 5:
			value = matrix[1][5]
		elif idx == 6:
			value = max(matrix[6]) - min(matrix[6])
		elif idx == 9:
			value = matrix[6][9]
		elif idx == 10:
			value = matrix[6][10]
		elif idx == 11:
			value = matrix[6][11]
	elif case == 2:
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
	elif case == 3:
		if idx == 1 or idx == 2 or idx == 3 or idx == 4:
			value = max(matrix[idx]) - min(matrix[idx])
		elif idx == 5:
			value = matrix[1][5]
		elif idx == 6:
			value = matrix[2][6]
		elif idx == 7:
			value = matrix[3][7]
		elif idx == 8:
			value = matrix[4][8]
	weights = round(random.uniform(value * 0.8, value * 1.2), 4)
	return weights

def getChangeIndex(now, R, total_cnt):
	for_use = []
	used = [0 for i in range(total_cnt)]
	idx = random.randint(0, 5)
	
	for i in range(R):
		cnt = 0
		while used[idx] != 0:
			cnt += 1
			if now % 2 == 0 or cnt > 4:
				right = total_cnt -1
			else:
				right = 5
			idx = random.randint(0, right)
		used[idx] = 1
		for_use += [weight_index[idx]]
	return for_use

def changeMatrix(for_use, matrix):
	for use in for_use:
		x, y = use
		value = matrix[x][y]
		change = random.uniform(value * 0.9, value * 1.1)
		change = round(change, 4)
		matrix[x][y] = matrix[y][x] = change
		#print(value, "->", change)
	return matrix

def delNodes(del_indexes):
	for delete in del_indexes:
		x, y = delete
		matrix[x][y] = matrix[y][x] = 0

def addPaddingAt(idx, weights, matrix):
	for m in matrix:
		m += [0.0]
	matrix.append([0.0 for i in range(len(matrix)+1)])
	matrix[idx][len(matrix)-1] = matrix[len(matrix)-1][idx] = weights
	return matrix

case = int(input("case > "))
if case == 1:
	weight_index = [[1, 3], [1, 4], [1, 5], [6, 9], [6, 10], [6, 11], [2, 1], [2, 7], [2, 6], [2, 8]]
	modify_index = del_index = [3, 4, 5, 9, 10, 11, 7, 8]
	del_weight = [[1, 3], [1, 4], [1, 5], [6, 9], [6, 10], [6, 11], [2, 7], [2, 8]]
	add_index = [3, 4, 5, 9, 10, 11, 1, 6]
elif case == 2:
	weight_index = [[1, 2], [3, 5], [4, 7], [6, 10], [8, 11], [9, 12], [1, 3], [1, 4], [3, 6], [4, 8], [6, 9], [8, 9]]
	modify_index = [2, 5, 7, 10, 11, 12] #[2, 5, 7, 10, 11, 12, 1, 3, 4, 6, 8, 9]
	del_index = [2, 5, 7, 10, 11, 12]
	del_weight = [[1, 2], [3, 5], [4, 7], [6, 10], [8, 11], [9, 12]]
	add_index = [2, 5, 7, 10, 11, 12, 1, 3, 4, 6, 8, 9]
elif case == 3:
	weight_index = [[1, 2], [1, 3], [1, 4], [1, 5], [2, 3], [2, 4], [2, 6], [3, 4], [3, 7], [4, 8]]
	modify_index = del_indx = [5, 6, 7, 8]
	del_weight = [[1, 5], [2, 6], [4, 8], [3, 7]]
	add_index = [5, 6, 7, 8, 1, 2, 3, 4]
total_cnt = len(weight_index)

upper_case = ['0'] + list(string.ascii_uppercase)
read_dir = 'represent/'
read_file = read_dir + 'original6.txt'
read_data = []
with open(read_file, 'r') as rf:
	for line in rf.readlines():
		read_data.append(list(map(float, line.split(' '))))

write_dir = 'datasets/group6/6'
length = len(read_data)
count = 0

write_file = write_dir + 'graph'
for i in range(150):
	count += 1
	filename = write_file + str(count) + '.txt'
	select = random.choice([1, 1, 1, 2])
	modify_R = getR()
	print('modif', modify_R)
	del_R = getR()
	add_R = getR()
	weight_R = random.randint(2, 4)
	
	use_alpha = upper_case[:length]
	if select != 1:
		use_alpha = getUseAlphaWith(i, use_alpha, modify_R)
	
	matrix = copy.deepcopy(read_data)
	if weight_R > 0:
		for_use = getChangeIndex(i, weight_R, total_cnt)
		matrix = changeMatrix(for_use, matrix)
	
	if del_R > 0:
		del_indexes = getDelIndex(del_R)
		delNodes(del_indexes)

	if add_R > 0:
		if i % 2 == 0:
			idx = random.choice(add_index)
		else:
			if case == 3:
				idx = random.choice(add_index[:4])
			else:
				idx = random.choice(add_index[:6])
		weights = getAddWeights(idx)
		matrix = addPaddingAt(idx, weights, matrix)
		alpha = list(string.ascii_uppercase)[random.randint(1, 24)]
		use_alpha += [alpha]
	
	writeFile(filename, matrix, use_alpha)