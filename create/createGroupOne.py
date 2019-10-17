import random as rd
from datetime import datetime

dir = 'group/'
filename = 'graph'
read = readfile = 'represent/original'

def createGroupData(matrix, cases):
	#rd.seed(rd.randint(10, 10000))
	length = len(matrix)
	num = round(rd.uniform(1, 15), rd.randint(1, 3))
	plus = round(rd.uniform(1, 5), rd.randint(1, 3))
	#print(num)
	for i in range(length):
		for j in range(i+1, length):
			if matrix[i][j] != 0:
				if cases < 45:
					num = round(rd.uniform(0,20), 2)
					while num == 0:
						num = round(rd.uniform(0, 20), 2)
					matrix[i][j] = matrix[j][i] = num
				elif cases < 95:
					num += plus
					matrix[i][j] = matrix[j][i] = round(rd.uniform(1, 15), 2)
				else:
					matrix[i][j] = matrix[j][i] = round(num + rd.uniform(0, 10), 2)
				

def fileWrite(matrix, count):
	with open(dir + filename + str(count) + '.txt', 'w') as file:
		for m in matrix:
			file.write(' '.join(str(i) for i in m) + "\n")

count = 0
for i in range(1, 7):	
	read = readfile + str(i) + ".txt"
	with open(read, 'r') as f:
		lines = f.readlines()
		length = len(lines)
		matrix = []
		for line in lines:
			matrix.append(list(map(int, line.replace('\n', '').split(' '))))
		#print(matrix)
		for t in range(180):
			if t < 145:
				createGroupData(matrix, t)
				fileWrite(matrix, count)
			count += 1


