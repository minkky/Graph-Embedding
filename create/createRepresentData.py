
test = [[0 for i in range(11)] for i in range(11)]
maxi = -1
while True:
	inp = input()
	if inp == 'end':
		break
	a, b = list(map(int, inp.split(' ')))
	test[a][b] = test[b][a] = 1
	maxi = max(maxi, max(a, b))

with open('representative/original5.txt', 'w') as file:
	for t in test[:maxi+1]:
		file.write(' '.join(str(i) for i in t[:maxi+1]) + "\n")
