# -*- coding: utf-8 -*-
"""Eye_lstm.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xk6Qi0jFc849Z40auIN88AiWoC9cBX5l
"""

# Commented out IPython magic to ensure Python compatibility.
#IMPORTS
import numpy as np
import pandas as pd
import cv2
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from keras.layers import Dropout
# %tensorflow_version 2.x
from tensorflow import keras
import tensorflow as tf
import time
from sklearn.model_selection import train_test_split

#import dataset 
df=pd.read_excel('lstm_eye.xlsx')

df.shape

#extract values 
values = df.values
values=values.astype('float32')
#split features and target value 
X=values[:,:-1]
Y=values[:,6:]
print(X.shape)
print(Y.shape)

#train test split
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.15, random_state=4)

#reshape for LSTM model
x_train = x_train.reshape((x_train.shape[0], 1, x_train.shape[1]))
x_test= x_test.reshape((x_test.shape[0], 1, x_test.shape[1]))
print(x_train.shape, y_train.shape,  x_test.shape, y_test.shape)

#create model 
model = Sequential()
model.add(LSTM(50, input_shape=(x_train.shape[1],x_train.shape[2])))
model.add(Dense(50, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# implement early stopping and train model 
es = keras.callbacks.EarlyStopping(monitor='accuracy', mode='max', verbose=1,patience=25,restore_best_weights=True)
model.fit(x_train, y_train, epochs=4000,batch_size=32,callbacks=[es])

model.evaluate(x_test, y_test)

model.predict(x_test)

model.save('model_eye')

!zip -r /content/model_eye.zip /content/model_eye

