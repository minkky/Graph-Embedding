import random as rd
from datetime import datetime
import glob, os

dirs = 'group/'
filename = 'graph'
extension = '.txt'
start = 500
files = []
for i in range(0, 500, 100):
	for j in range(0, 5):
		files.append(i+j)
files = [dirs + filename + str(name) + extension for name in files]
#print(files)

for file in files:
	with open(file) as f:
		new_file = open(dirs + filename + str(start) + extension, 'w')
		for line in f.readlines():
			for index, num in enumerate(line.replace('\n','').split(' ')):
				if float(num) != 0:
					if float(num) < 10:
						new_file.write(str(round(float(num) + 50, 2)))
					else:
						new_file.write(num)
				else:
					new_file.write('0')
				if index != len(line.split(' '))-1:
					new_file.write(" ")
			new_file.write('\n')
		start += 1
