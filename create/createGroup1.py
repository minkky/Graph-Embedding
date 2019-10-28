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
		cnt = 0
		while used[idx] != 0 or weight_index[idx] in del_indexes:
			cnt += 1
			if now % 2 == 0 or cnt > 4:
				right = total_cnt -1
			else:
				right = 5
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

def getModiOrDelIndexes(count):
	if count % 2 == 0:
		right = 7
	else:
		right = 5
	idx = random.randint(0, right)
	idx1 = random.randint(0, right)
	while idx == idx1:
		idx = random.randint(0, right)
	return idx, idx1

def getUseAlphaWith(index, use_alpha):
	arr = [0, 0, 0, 0, 1, 1, 1, 2]
	random.shuffle(arr)
	modify_R = random.choice(arr)
	random.shuffle(arr)
	add_R = random.choice(arr)
	print('modi R, add R', modify_R, add_R)
	
	idx, idx1 = getModiOrDelIndexes(index)
	for r in range(modify_R):
		use_alpha[modify_index[idx]] = list(string.ascii_uppercase)[random.randint(1, 24)]
		idx = idx1
	
	alpha = list(string.ascii_uppercase)[random.randint(1, 24)]
	use_alpha += [alpha]
	return use_alpha

def getDelIndex(count):
	idx, idx1 = getModiOrDelIndexes(count)
	indexes = []
	for r in range(count):
		indexes.append(del_weight[idx])
		idx = idx1
	return indexes

def getAddWeights(idx):
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
	weights = round(random.uniform(value * 0.8, value * 1.2), 4)
	return weights

def addPaddingAt(idx, weights, matrix):
	for m in matrix:
		m += [0.0]
	matrix.append([0.0 for i in range(len(matrix)+1)])
	matrix[idx][len(matrix)-1] = matrix[len(matrix)-1][idx] = weights
	return matrix

weight_index = [[1, 3], [1, 4], [1, 5], [6, 9], [6, 10], [6, 11], [2, 1], [2, 7], [2, 6], [2, 8]]
modify_index = del_index = [3, 4, 5, 9, 10, 11, 7, 8]
del_weight = [[1, 3], [1, 4], [1, 5], [6, 9], [6, 10], [6, 11], [2, 7], [2, 8]]
add_index = [3, 4, 5, 9, 10, 11, 1, 6]
total_cnt = len(weight_index)

upper_case = ['0'] + list(string.ascii_uppercase)
read_dir = 'represent/'
read_file = read_dir + 'original1.txt'
read_data = []
with open(read_file, 'r') as rf:
	for line in rf.readlines():
		read_data.append(list(map(float, line.split(' '))))

write_dir = 'datasets/group1/1'
count = 0
for mode in range(1, 5): #4
	write_file = write_dir + 'graph'
	length = len(read_data)
	print("**mode**")
	for i in range(25):
		#print('alpha', use_alpha)
		select = random.choice([1, 1, 1, 2])
		use_alpha = upper_case[:length]
		if select != 1:
			use_alpha = getUseAlphaWith(i, use_alpha)
		print(use_alpha)		

		arr = [0, 0, 0, 0, 0, 0, 1, 1, 1, 2]
		random.shuffle(arr)

		del_R = random.choice(arr)
		print('del R : ', del_R)

		filename = write_file + str(count+1) + '.txt'
		count += 1
		if del_R != 0:
			del_indexes = getDelIndex(del_R)
		else:
			del_indexes = []
		matrix = copy.deepcopy(read_data)
		if i % 2 == 0:
			idx = random.choice(add_index)
		else:
			idx = random.choice(add_index[:6])
		
		weights = getAddWeights(idx)
		#print(idx, weights)
		matrix = addPaddingAt(idx, weights, matrix)
		weight_R = random.randint(2, 4)
		for_use = getChangeIndex(i, weight_R, total_cnt, del_indexes)
		changeAndSaveMatrix(for_use, matrix)
