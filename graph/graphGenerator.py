###
# This is a QnD script to generate "random" adjacency list and heuristic files.
#
#!/bin/python
#
import sys
import random
from math import sqrt

if len(sys.argv) < 7:
    print("Usage: python gg.py <x> <y> <num_nodes> <max_branch> <src> <dst>")
    print("Nodes will be numbered 1 to num_nodes, src and dst must be between these two values")
    exit()

x = int(sys.argv[1])
y = int(sys.argv[2])

num_nodes = int(sys.argv[3])
max_branch = int(sys.argv[4])

src = int(sys.argv[5])
dst = int(sys.argv[6])

points = []

while len(points) < num_nodes:
    point_x = random.randint(1, x)
    point_y = random.randint(1, y)

    if (point_x, point_y) not in points:
        points.append((point_x,point_y))


nodes = {}

points.sort()

name = 1
for p in points:
    nodes[name] = p
    name += 1

al = []

for n in nodes.keys():
    for i in range(random.randint(1, max_branch)):
        from_ = n
        to = random.choice(nodes.keys())

        while to == from_:
            to = random.choice(nodes.keys())

        cost = round(sqrt((nodes[to][0] - nodes[from_][0])**2 + (nodes[to][1] - nodes[from_][1])**2),3)

        al.append(str(to) + " " + str(from_) + " " + str(cost))

al_name = "gg_" + sys.argv[1] + "x" + sys.argv[2] + ".al"
#heu_name = "gg_" + sys.argv[1] + "x" + sys.argv[2] + ".heu"

f = open(al_name, "w")
for a in al:
    f.write(a)
    if a != al[-1]:
        f.write("\n")
f.close()
'''
heus = []

for n in nodes.keys():
    heus.append(str(n) + " " + str(round(sqrt((nodes[n][0] - nodes[dst][0])**2 + (nodes[n][1] - nodes[dst][1])**2),3)))


f = open(heu_name, "w")

for h in heus:
    f.write(h)
    if h != heus[-1]:
        f.write("\n")

f.close()
'''
print("Created a graph of " + str(len(nodes)) + " nodes and " + str(len(al)) + " edges.")


