import random as rd
from datetime import datetime

dir = 'groupData/'
filename = 'pgraph'
read = readfile = 'original'

def createGroupData(matrix):
	rd.seed(rd.randint(10, 10000))
	length = len(matrix)
	num = round(rd.uniform(1, 3), 2)
	print(num)
	for i in range(length):
		for j in range(i+1, length):
			if matrix[i][j] != 0:
				if rd.choice([False, True, False, False, False]):
					num = round(num + rd.randint(1, 5), 2)
				else:
					if rd.choice([False, True, False, True, False]):
						num = round(num + rd.uniform(num, 10), 2)
					else:
						num = round(num - rd.uniform(num, 10), 2)
						while int(num) <= 0:
							num = rd.randint(0, 3)
							num = round(num + rd.uniform(num, 10), 2)	
				matrix[i][j] = matrix[j][i] = num
	#print(matrix)

def fileWrite(matrix, count):
	with open(dir + filename + str(count) + '.txt', 'w') as file:
		for m in matrix:
			file.write(' '.join(str(i) for i in m) + "\n")

count = 0
for i in range(10):	
	read = readfile + str(i) + ".txt"
	with open(read, 'r') as f:
		lines = f.readlines()
		length = len(lines)
		matrix = []
		for line in lines:
			matrix.append(list(map(int, line.replace('\n', '').split(' '))))
		#print(matrix)
		for t in range(15):
			createGroupData(matrix)
			fileWrite(matrix, count)
			count += 1