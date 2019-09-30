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
from keras.models import load_model
from keras.optimizers import Adam
from keras.layers import Input, Lambda
from keras.models import Model
from keras import losses
import keras.backend.tensorflow_backend as K
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

class Graph:
	def __init__(self, n_features, epochs, steps_per_epoch, max_sequence_length):
		self.n_features = n_features
		self.epochs = epochs
		self.steps_per_epoch = steps_per_epoch
		self.max_sequence_length = max_sequence_length

	def repeat_vector(self, args):
		layer_to_repeat = args[0]
		sequence_layer = args[1]
		return RepeatVector(K.shape(sequence_layer)[1])(layer_to_repeat)	
	
	def custom_loss(self, y_true, y_pred):
		loss1 = losses.mean_squared_error(y_true, y_pred)
		#loss2 = losses.categorical_crossentropy(y_true, y_pred)
		return loss1

	def model(self):
		inputs = Input(shape=(None, 3))
		encoded = LSTM(128, return_sequences=True)(inputs)  #activation 안적으면 tanh
		encoded = LSTM(64)(encoded)
		decoded = Lambda(self.repeat_vector, output_shape=(None, 64)) ([encoded, inputs]) # inputs의 shape[1] 만큼 encoded 를 반복 생성
		decoded = LSTM(64, return_sequences=True)(decoded)
		decoded = LSTM(128, return_sequences=True)(decoded)
		decoded = TimeDistributed(Dense(3))(decoded)
		#encoder = Model(inputs, encoded)
		#lstm_autoencoder = 
		lstm_autoencoder = Model(inputs, decoded)
		return lstm_autoencoder
	
	def setModel(self, model):
		self.lstm_autoencoder = model

	def getModel(self):
		return self.lstm_autoencoder

	#def compile(self, loss, optimizer):
	#	lstm_autoencoder.compile(loss=loss, optimizer=optimizer)

	def train_generator(self, x_train):
		idx = 0
		while True:
			yield np.array([x_train[idx]]), np.array([x_train[idx]])
			idx +=1
			if idx >= len(x_train):
				idx = 0

	def training(self):
		lstm_autoencoder = self.model()
		self.setModel(lstm_autoencoder)
		lstm_autoencoder.compile(loss='mse', optimizer='adam')
		lstm_autoencoder.fit_generator(self.train_generator(x_train), epochs=self.epochs, steps_per_epoch=self.steps_per_epoch, verbose=1)

		if input('save ?(y or n) ') == 'y':
			path = input('path: ')
			with open(path + '.json', 'w') as file:
				file.write(lstm_autoencoder.to_json())
			lstm_autoencoder.save_weights(path+'_weights.h5')
			#self.save(path, lstm_autoencoder)

	def check_mse(self):
		mean= 0
		for xt in x_test:
			xt = np.array(xt)
			xt = xt.reshape(1, xt.shape[0], xt.shape[1])
			out = self.lstm_autoencoder.predict(xt)
			mean += ((xt-out)**2).mean(axis=None)
		total_test_loss = mean / len(x_test)
		return total_test_loss

	def save(self, path, model):
		#print(self.lstm_autoencoder.summary())
		#model_json = self.lstm_autoencoder.to_json()
		with open(path + '.json', 'w') as file:
			file.write(model.to_json())
		#multi_model = multi_gpu_model(model, gpus=1)
		#model.set_weights(multi_model.get_weights())
		model.save_weights(path + '_weights.h5')

	def load(self, path1, path2):
		model = model_from_json(open(path1).read())
		model.load_weights(path2)
		return model

class GraphSequence:
	def getData(self, dir):
		all_data = []
		sequence_length = []
		name = []
		for file in sorted(glob.glob(dir)):
			name.append(file.split('/')[-1].replace('.txt', ''))
			datasets = []
			for f in open(file, 'r'):
				(u, v, w) = f[1:-2].split(',')
				datasets.append([int(u), int(v), float(w)])
			sequence_length.append(len(datasets))
			all_data.append(datasets)
		
		x_train, x_test, train_name, test_name = train_test_split(all_data, name, test_size=0.3)
		#x_test, x_val, test_name, val_name = train_test_split(x_test, test_name, test_size=0.33)
		return x_train, x_test, train_name, test_name, sequence_length

	def getLengthWithXtrain():
		return len(x_train)

	def getMaxLengthWithSequence():
		return max(sequence_length)


dir = './latest_sequence/bfs/*'
graphSeq = GraphSequence()
x_train, x_test, train_name, test_name, sequence_length = graphSeq.getData(dir)

model = Graph(3, 1, len(x_train), max(sequence_length))
#model.model()
#model.compile('mse', 'adam')
model.training()
total_test_loss = model.check_mse()
print('test loss', total_test_loss)
'''
if input('save ?(y or n) ') == 'y':
	path = input('path: ')
	model.save(path)
'''