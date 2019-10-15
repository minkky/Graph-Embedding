import copy as cp
import glob, os, string
import random as rd

def writeFile(use_alpha, write_name, read_name):
	with open(write_name, 'w') as wf:
		with open(read_name, 'r') as f:
			for line in f.readlines():
				a, b, w = line[1:len(line)-2].split(', ')
				l = str([use_alpha[int(a)-1], use_alpha[int(b)-1], float(w)]) + "\n"
				wf.write(l)

def getAlphaWith(number, leng):
	use_alpha = []
	if number == 1:
		use_alpha = alpha[:leng]
	elif number == 2:
		tmp = alpha[:leng]
		for k in range(leng):
			use_alpha.append(tmp[rd.randint(0, leng-1)])	
	else:
		use_alpha = []
		for k in range(leng):
			use_alpha.append(alpha[rd.randint(0, len(alpha)-1)])
	rd.shuffle(use_alpha)

	return use_alpha

filename = "../latest_sequence/bfs/graph"
dir_name = "../latest_sequence/bfs-character/"
name = "graph"

alpha = list(string.ascii_uppercase)
for_use = []

for i in range(0, 900, 150):
	names = [j for j in range(i, i+150)]		

	first = [0 for k in range(50)] + [1 for k in range(10)]
	sec = [0 for k in range(30)] + [1 for k in range(10)]
	thr = [0 for k in range(40)] + [1 for k in range(10)]
	choices = first + sec + thr

	rd.shuffle(first)
	rd.shuffle(sec)
	rd.shuffle(thr)
	rd.shuffle(names)
	
	for index, j in enumerate(names):
		files = glob.glob(filename+str(j)+"-*")
		leng = len(files)
		
		if choices[index] == 1:
			for_use.append(j)
	
		if index < i + 60:
			use_alpha = getAlphaWith(1, leng)
		elif index < i + 100:
			use_alpha = getAlphaWith(2, leng)
		elif index < i + 150:
			use_alpha = getAlphaWith(3, leng)
		
		for file in files:
			write_name = dir_name + file.split('/')[3]
			writeFile(use_alpha, write_name, file)

# 각 label 생성 방법 (1, 2, 3) 가운데 방법별 10가지를 뽑아와 다른 방법 형태로 변경하여 주기
gname = "graph"
index = 899
for i in range(0, 180, 30):
	for j in range(i, i+30):
		files = glob.glob(filename + str(for_use[j]) +"-*")
		leng = len(files)
		index += 1
		if j < i + 10:
			# 2번 3번
			use_alpha1 = getAlphaWith(2, leng)
			use_alpha2 = getAlphaWith(3, leng)
			for file in files:
				idx = file.split('-')[1]
				write_name1 = dir_name + gname + str(index) + "-" + str(idx)
				write_name2 = dir_name + gname + str(index+1) + "-" + str(idx)
				writeFile(use_alpha1, write_name1, file)
				writeFile(use_alpha2, write_name2, file)
		elif j < i + 20:
			# 1번 3번
			use_alpha1 = getAlphaWith(1, leng)
			use_alpha2 = getAlphaWith(3, leng)
			for file in files:
				idx = file.split('-')[1]
				write_name1 = dir_name + gname + str(index) + "-" + str(idx)
				write_name2 = dir_name + gname + str(index+1) + "-" + str(idx)
				writeFile(use_alpha1, write_name1, file)
				writeFile(use_alpha2, write_name2, file)
		else:
			# 1번 2번
			use_alpha1 = getAlphaWith(1, leng)
			use_alpha2 = getAlphaWith(2, leng)
			for file in files:
				idx = file.split('-')[1]
				write_name1 = dir_name + gname + str(index) + "-" + str(idx)
				write_name2 = dir_name + gname + str(index+1) + "-" + str(idx)
				writeFile(use_alpha1, write_name1, file)
				writeFile(use_alpha2, write_name2, file)
		index += 1
			