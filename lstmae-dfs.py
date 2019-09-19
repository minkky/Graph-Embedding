#!/usr/bin/env python
# coding: utf-8

import numpy as np
import glob, os
from keras import layers as ly
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import RepeatVector
from keras.layers import TimeDistributed
from keras.preprocessing import sequence
from sklearn.model_selection import train_test_split
import keras.backend.tensorflow_backend as K
from keras.optimizers import Adam
from keras.layers import Input, LSTM, RepeatVector, Lambda
from keras.models import Model

dir = './new_sequence_dfs/*'

# file read
all_data = []
sequence_length = []
name = []
for file in sorted(glob.glob(dir)):
    name.append(file.split('/')[2].replace('.txt', ''))
    datasets = []
    for f in open(file, 'r'):
        f = f.replace(']', '').replace('[', '').replace('\n','')
        (u, v, w) = f.split(',')
        datasets.append([int(u), int(v), float(w)])
    sequence_length.append(len(datasets))
    all_data.append(datasets)
#all_data = np.array(all_data)
all_data = np.array([np.array(arr) for arr in all_data])

x_train, x_test, train_name, test_name = train_test_split(all_data, name, test_size=0.3)
x_test, x_val, test_name, val_name = train_test_split(x_test, test_name, test_size=0.33)


n_features = 3
#batch_size = 32
epochs = 500
steps_per_epoch = len(x_train)

def repeat_vector(args):
    layer_to_repeat = args[0]
    sequence_layer = args[1]
    return RepeatVector(K.shape(sequence_layer)[1])(layer_to_repeat)

inputs = Input(shape=(None, n_features))
encoded = LSTM(128, return_sequences=True)(inputs)  #activation 안적으면 tanh
encoded = LSTM(64, return_sequences=True)(encoded)
encoded = LSTM(32, activation='relu')(encoded)

decoded = Lambda(repeat_vector, output_shape=(None, 32)) ([encoded, inputs]) # inputs의 shape[1] 만큼 encoded 를 반복 생성

decoded = LSTM(32, return_sequences=True)(decoded)
decoded = LSTM(64, return_sequences=True)(decoded)
decoded = LSTM(128, return_sequences=True)(decoded)
decoded = TimeDistributed(Dense(n_features))(decoded)
encoder = Model(inputs, encoded)

lstm_autoencoder = Model(inputs, decoded)
lstm_autoencoder.compile(loss='mean_squared_error', optimizer=Adam(lr=0.001))

def train_generator(x_train):
    idx = 0
    while True:
        yield np.array([x_train[idx]]), np.array([x_train[idx]])
        idx +=1
        if idx >= len(x_train):
            idx = 0
lstm_autoencoder.fit_generator(train_generator(x_train), epochs=epochs, steps_per_epoch=steps_per_epoch, verbose=1)#, validation_data=val_generator(x_val))

''' result
    epoch 500, 0.0624
    epoch 1000, 0.0448
    (256, 128, 64, 64, 128, 256) epoch 100 5.2650 
    (128, 64, 32, 32, 64, 128) epoch 500 
'''

'''
encoder = Model(inputs, encoded)


lstm_autoencoder.summary()


encoder.summary()


x_test[0]


lstm_autoencoder.predict(x_test[0].reshape(1, x_test[0].shape[0], x_test[0].shape[1]))


test = x_test[0].reshape(1, 9, 3)
latent_vector = []
for x in x_test:
    x = x.reshape(1, x.shape[0], x.shape[1])
    latent_vector.append(encoder.predict(x)[0])


def printMatrix(matrix):
    length = int(max(max(matrix[:, 0]), max(matrix[:, 1])))
    adj = [[0 for i in range(length)] for i in range(length)]
    
    for m in matrix:
        (i, j, w) = m
        i = int(i) -1
        j = int(j) -1
        adj[i][j] = adj[j][i] = w
    for i in range(length):
        for j in range(length):
            print(str(adj[i][j]), end=',')
        print()
    print("===============")


# sequence to matrix
for index, x in enumerate(x_test):
    print("#", str(index))
    printMatrix(x)
    


standard = latent_vector[0]


import copy
dist = []
left = 100000
right = -10000
for index, v in enumerate(latent_vector[1:]):
    d = round(euclidean_distance(standard, v), 8)
    dist.append(d)
    if d > right:
        right= d
    if left > d:
        left = d
dist1 = copy.deepcopy(dist)
dist1.sort()
#print(dist, dist1)
for index, d in enumerate(dist1):
    print( (index+1, dist.index(d)+1), end='  ')


def euclidean_distance(a, b):
    return np.sqrt(np.sum(a-b) ** 2)


len(x_test)




'''