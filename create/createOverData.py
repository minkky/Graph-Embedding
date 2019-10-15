import random as rd
import copy
from datetime import datetime

dir = 'group/'
filename = 'graph'
read = readfile = 'group/graph'

def createGroupData(matrix, cases):
	#rd.seed(rd.randint(10, 10000))
	length = len(matrix)
	num = round(rd.uniform(1, 15), rd.randint(1, 3))
	plus = round(rd.uniform(1, 5), rd.randint(1, 3))
	#print(num)
	for i in range(length):
		for j in range(i+1, length):
			if matrix[i][j] != 0:
				if cases < 30:
					num = round(rd.uniform(0,20), 2)
					while num == 0:
						num = round(rd.uniform(0, 20), 2)
					matrix[i][j] = matrix[j][i] = num
				elif cases < 55:
					num += plus
					matrix[i][j] = matrix[j][i] = round(num, 2)
				elif cases < 100:
					matrix[i][j] = matrix[j][i] = round(num + rd.uniform(0, 10), 2)
				

def fileWrite(matrix, count):
	with open(dir + filename + str(count) + '.txt', 'w') as file:
		for m in matrix:
			file.write(' '.join(str(i) for i in m) + "\n")

count = 0
for i in range(125, 900, 150):
	for j in range(i, i+25):
		read = readfile + str(rd.randint(i-125, i-1)) +".txt"
		matrix = []
		with open(read, 'r') as f:
			for line in f.readlines():
				row = []
				for each in list(map(float, line.split(' '))):
					if each != 0.0:
						row.append(round(each + rd.uniform(10, 50), 2))
					else:
						row.append(0)
				matrix.append(row)
				fileWrite(matrix, j)