import os
import random as rd

count = 0
for i in range(5, 11):
	for j in range(0, 15):
		count += 1
		num = rd.randint(i, i+5)
		param = str(i) + " " + str(i) + " " + str(i) + " " + str(num) + " " + str(1) + " " + str(i)
		os.system('python graphGenerator.py ' + param)
		os.system('python pairToAdjacency.py ' + str(i) + ' ' + str(count))	