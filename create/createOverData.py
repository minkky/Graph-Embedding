import random as rd
import copy
from datetime import datetime

dir = 'group/'
filename = 'graph'
read = readfile = 'group/graph'		

def fileWrite(matrix, count):
	with open(dir + filename + str(count) + '.txt', 'w') as file:
		for m in matrix:
			file.write(' '.join(str(i) for i in m) + "\n")

count = 0
for i in range(125, 1260, 210):
	for j in range(i, i+25):
		#print(j, rd.randint(i-145, i-1))
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
		