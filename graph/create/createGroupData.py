import random as rd
from datetime import datetime

dir = 'groupData1/'
filename = 'pgraph'
read = readfile = 'original'

def createGroupData(matrix, cases):
	rd.seed(rd.randint(10, 10000))
	length = len(matrix)
	num = round(rd.uniform(1, 5), rd.randint(1, 2))
	print(num)
	for i in range(length):
		for j in range(i+1, length):
			if matrix[i][j] != 0:
				if cases < 6:
					num = round(num + j , rd.randint(1, 2))
					matrix[i][j] = matrix[j][i] = num
				elif cases <= 10:
					num = round(num - j, 2)
					while num <= 0:
						num = num * -1
						if num == 0:
							num -= j
					matrix[i][j] = matrix[j][i] = num
				else:
					num = round(num + rd.randint(1, 5), rd.randint(1, 2))
				
				'''
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
				'''
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
		for t in range(10):
			createGroupData(matrix, t)
			fileWrite(matrix, count)
			count += 1