
test = [[0 for i in range(13)] for i in range(13)]
maxi = -1
while True:
	inp = input('u v: ')
	if inp == 'end':
		break
	a, b= list(map(int, inp.split(' ')))
	test[a][b] = test[b][a] = float(input('weight: '))
	maxi = max(maxi, max(a, b))

with open('represent/original3.txt', 'w') as file:
	for t in test[:maxi+1]:
		file.write(' '.join(str(i) for i in t[:maxi+1]) + "\n")
