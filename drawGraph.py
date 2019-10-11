#!/usr/bin/env python
# coding: utf-8

import numpy as np
import glob, os
from keras import layers as ly
from keras.models import Sequential, load_model, Model
from keras.layers import Input, Lambda, LSTM, Dense, RepeatVector, TimeDistributed
from keras.preprocessing import sequence
from sklearn.model_selection import train_test_split
from keras.optimizers import Adam
import copy
from scipy.spatial.distance import cosine as cosine_distance
from keras.models import model_from_json
from collections import Counter
import import_ipynb
import drawingGraph as G
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

def getIndexFromGraph(filename):
    index = int(filename.split('-')[0].replace('graph', ''))
    return index

def calculateGraphGroup(num_dict):
    for index, data in enumerate(all_data):
        loc = getIndexFromGraph(graph_group[index])
        num_dict[loc] += 1
    return num_dict

def getEmbeddingSum():
    sum_embedding = [[0 for i in range(embedded_length)] for i in range(graph_length)]
    for index, data in enumerate(all_data):
        data = data.reshape(1, data.shape[0], data.shape[1])
        embedded = encoder.predict(data)
        loc = getIndexFromGraph(graph_group[index])
        sum_embedding[loc] += embedded.reshape(embedded.shape[1])
    return sum_embedding

def getEmbeddingAvg():
    avg_embedding = [[0 for i in range(embedded_length)] for i in range(graph_length)]
    sum_embedding = getEmbeddingSum()
    for index in range(graph_length):
        avg_embedding[index] = sum_embedding[index] / num_dict[index]
    return avg_embedding

def getEmbeddingVector(index):
    data_index = []
    data = []
    counts = num_dict[index]
    for num, i in enumerate(graph_group):
        if index == getIndexFromGraph(i):
            data_index.append(num)
        if len(data_index) == counts:
            break
    for i in data_index:
        dt = all_data[i].reshape(1, all_data[i].shape[0], all_data[i].shape[1])
        dt = encoder.predict(dt)
        dt = dt.reshape(dt.shape[1])
        data.append(dt)
    return data

def getMode(values):
    values.sort()
    mode = Counter(values).most_common()
    maximum = mode[0][1]
    if maximum == 1:
        return values.mean()
    else:
        dt = []
        for m in mode:
            if maximum == m[1]:
                dt.append(m[0])
            else:
                break
        return np.array(dt).mean()

def getEmbeddingMode(): # 최빈값
    mode_embedding = [[0 for i in range(embedded_length)] for i in range(graph_length)]
    for index in range(graph_length):
        vectors = np.array(getEmbeddingVector(index))
        for count in range(embedded_length):
            values = vectors[:, count:count+1].reshape(num_dict[index])
            mode_embedding[index][count] = getMode(values)
        mode_embedding[index] = np.array(mode_embedding[index])
    return mode_embedding

def getEmbeddingExceptMinMax():
    except_embedding = [[0 for i in range(embedded_length)] for i in range(graph_length)]
    for index in range(graph_length):
        vectors = np.array(getEmbeddingVector(index))
        for count in range(embedded_length):
            values = vectors[:, count:count+1].reshape(num_dict[index])
            values.sort()
            except_embedding[index][count] =  values[1:-1].mean()
        except_embedding[index] = np.array(except_embedding[index])
    return except_embedding

def euclidean_distance(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.sqrt(np.sum(a-b) ** 2)

def getGraphOrder(dist):
    ordered = copy.deepcopy(dist)
    ordered.sort()
    
    names = []
    
    for item in ordered:
        for index, d in enumerate(dist):
            if item == d:
                names.append(index)#+1)
                break
    return names, ordered

def getDistFromEmbedding(distance_measure, embedding, obj):
    if embedding  == 'sum':
        embeddings = sum_embedding
    elif embedding == 'avg':
        embeddings = avg_embedding
    elif embedding == 'mode':
        embeddings = mode_embedding
    elif embedding =='except':
        embeddings = except_embedding
    
    dist = []
    for embed in embeddings:
        if distance_measure == 'euc':
            dist.append(euclidean_distance(obj, embed))
        else:
            dist.append(cosine_distance(obj, embed))
    return dist

def getTopData(n, datasets, names):
    data = []
    for n in names[:n+1]:
        data.append(datasets[n])
    return data

def draw(drawobj, drawobj_name, dir_name, save):
    for index, obj in enumerate(drawobj):
        G.drawGraph(dir_name, 'graph' + str(drawobj_name[index]), index, obj, save)

filename = input('filename: ')
json_file = open("result/mse_weights/last_mse_lstmae.json", "r") #"+filename+"
loaded_model_json = json_file.read() 
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights('result/mse_weights/'+ filename + '.h5')
sequence_type = input('type(bfs? dfs?): ')
if sequence_type == 'dfs':
    dir = './latest_sequence/dfs/*'
else:
    dir = './latest_sequence/bfs/*'

# file read
all_data = []
sequence_length = []
graph_group = []
for file in sorted(glob.glob(dir)):
    graph_group.append(file.split('/')[-1].replace('.txt', ''))
    datasets = []
    for f in open(file, 'r'):
        (u, v, w) = f[1:-2].split(',')
        datasets.append([int(u), int(v), float(w)])
    sequence_length.append(len(datasets))
    all_data.append(datasets)
all_data = np.array([np.array(arr) for arr in all_data])

graph_length = len(glob.glob('./latest_graph_data/*'))
embedded_length = 64
lstm_autoencoder = loaded_model
encoder = Model(lstm_autoencoder.input, lstm_autoencoder.layers[2].output)
num_dict = { i:0 for i in range(graph_length)}
num_dict = calculateGraphGroup(num_dict)
sum_embedding = getEmbeddingSum()
avg_embedding = getEmbeddingAvg()
mode_embedding = getEmbeddingMode()
except_embedding = getEmbeddingExceptMinMax()
except_embedding = np.array(except_embedding)

#그래프 그리기 위해 각 그래프 그룹 가운데 하나씩 가져옴. (모든 노드에 대한 sequence 에서 하나의 노드 시퀀스만 가져오기) 
datasets = [[] for i in range(graph_length)]
for n, data in zip(graph_group, all_data):
    index = int(n.split('-')[0].replace('graph', ''))
    if len(datasets[index]) == 0:
        d = []
        for row in data:
            u, v, w = row
            d.append([int(u), int(v), float(w)])
        datasets[index] = d

import random as rd

for i in range(20, 101, 20):
    for idx in range(i):
        print(rd.randint(0, 501))
    #rd.randint(0, )

mode_obj = mode_embedding[456]
sum_obj = sum_embedding[456]
avg_obj = avg_embedding[456]
except_obj = except_embedding[456]
dist_avg_cos = getDistFromEmbedding('cos', 'avg', avg_obj)
names_avg_cos, ordered_avg_cos = getGraphOrder(dist_avg_cos)

dist_sum_cos = getDistFromEmbedding('cos', 'sum', sum_obj)
names_sum_cos, ordered_sum_cos = getGraphOrder(dist_sum_cos)

dist_mode_cos = getDistFromEmbedding('cos', 'mode', mode_obj)
names_mode_cos, ordered_mode_cos = getGraphOrder(dist_mode_cos)

dist_except_cos = getDistFromEmbedding('cos', 'except', except_obj)
names_except_cos, ordered_except_cos = getGraphOrder(dist_except_cos)
dist_avg_euc = getDistFromEmbedding('euc', 'avg', avg_obj)
names_avg_euc, ordered_avg_euc = getGraphOrder(dist_avg_euc)

dist_sum_euc = getDistFromEmbedding('euc', 'sum', sum_obj)
names_sum_euc, ordered_sum_euc = getGraphOrder(dist_sum_euc)

dist_mode_euc = getDistFromEmbedding('euc', 'mode', mode_obj)
names_mode_euc, ordered_mode_euc = getGraphOrder(dist_mode_euc)

dist_except_euc = getDistFromEmbedding('euc', 'except', except_obj)
names_except_euc, ordered_except_euc = getGraphOrder(dist_except_euc)
top10_mode_cos = getTopData(10, datasets, names_mode_cos)
back10_mode_cos = getTopData(10, datasets, names_mode_cos[::-1])

top10_sum_cos = getTopData(10, datasets, names_sum_cos)
back10_sum_cos = getTopData(10, datasets, names_sum_cos[::-1])

top10_avg_cos = getTopData(10, datasets, names_avg_cos)
back10_avg_cos = getTopData(10, datasets, names_avg_cos[::-1])

top10_except_cos = getTopData(10, datasets, names_except_cos)
back10_except_cos = getTopData(10, datasets, names_except_cos[::-1])
top10_mode_euc = getTopData(10, datasets, names_mode_euc)
back10_mode_euc = getTopData(10, datasets, names_mode_euc[::-1])

top10_sum_euc = getTopData(10, datasets, names_sum_euc)
back10_sum_euc = getTopData(10, datasets, names_sum_euc[::-1])

top10_avg_euc = getTopData(10, datasets, names_avg_euc)
back10_avg_euc = getTopData(10, datasets, names_avg_euc[::-1])

top10_except_euc = getTopData(10, datasets, names_except_euc)
back10_except_euc = getTopData(10, datasets, names_except_euc[::-1])
# check top n results
count = 0
print('    {:8s}{:8s}{:8s}{:s}'.format('sum',  'avg', 'mode','except(min, max)'))
for s, a, m, e in zip(names_sum_cos, names_avg_cos, names_mode_cos, names_except_cos):
#for s, a, m, e in zip(names_sum_cos[::-1], names_avg_cos[::-1], names_mode_cos[::-1], names_except_cos[::-1]):    
    #if s == 526 or a == 526 or m == 526 or e == 526:
    #    print(count)
    print('{:8d}{:8d}{:8d}{:8d}'.format(s, a, m, e))
    count += 1
    if count >= 21:
        break
count = 0
print('    {:8s}{:8s}{:8s}{:s}'.format('sum',  'avg', 'mode','except(min, max)'))
#for s, a, m, e in zip(names_sum_cos, names_avg_cos, names_mode_cos, names_except_cos):
for s, a, m, e in zip(names_sum_cos[::-1], names_avg_cos[::-1], names_mode_cos[::-1], names_except_cos[::-1]):    
    #if s == 526 or a == 526 or m == 526 or e == 526:
    #    print(count)
    print('{:8d}{:8d}{:8d}{:8d}'.format(s, a, m, e))
    count += 1
    if count > 21:
        break
        
print("cos mode")
draw(top10_mode_cos, names_mode_cos, '', False)
print("cos except min max")
draw(top10_except_cos, names_except_cos, '', False)
draw(top10_sum_cos, names_sum_cos, '', False)
draw(top10_avg_cos, names_avg_cos, '', False)
draw(back10_except_cos, names_except_cos[::-1], '', False)

'''

import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

sns.set_style('darkgrid')
sns.set_palette('muted')
sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 2.5})
labels = [str(i) for i in range(len(except_embedding)+1)]
tsne_train_xs = TSNE(n_components=2, verbose=1, perplexity=6, n_iter=1000).fit_transform(except_embedding, labels)
plt.figure(figsize=(8, 8))
plt.scatter(x = tsne_train_xs[:,0], y=tsne_train_xs[:,1], color=sns.color_palette("hls", len(except_embedding)))

#for i in [0, 525, 526]:
    #plt.annotate(str(i), (tsne_train_xs[i, 0], tsne_train_xs[i, 1]))
plt.show()
'''