#!/usr/bin/env python
# coding: utf-8

# In[2]:


import cv2
import numpy as np
import sys
import time
import pandas as pd
import matplotlib.pyplot as plt
import PIL
from PIL import Image
from scipy import ndimage, misc


# In[3]:


def moving_average(a, n=10) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n


# In[4]:


n = 10    #arbitrary
x,y = 32,32

X = np.zeros((n,x,y,3))
Y = np.zeros((n))


# In[5]:


# keras imports for the dataset and building our neural network
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2D, MaxPool2D, Flatten, BatchNormalization, MaxPooling2D
from keras.utils import np_utils
from keras.callbacks import EarlyStopping, ModelCheckpoint

# to calculate accuracy
from sklearn.metrics import accuracy_score

percentage = 90

# loading the dataset
X_train = X[:percentage*X.shape[0]//100]
X_test  = X[percentage*X.shape[0]//100:]

y_train = Y[:percentage*X.shape[0]//100]
y_test  = Y[percentage*X.shape[0]//100:]

# building the input vector from the 28x28 pixels
#X_train = X_train.reshape(X_train.shape[0], 28, 28, 1)
#X_test = X_test.reshape(X_test.shape[0], 28, 28, 1)
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')

# normalizing the data to help with the training
X_train /= 255
X_test /= 255

# one-hot encoding using keras' numpy-related utilities
n_classes = 2
print("Shape before one-hot encoding: ", y_train.shape)
Y_train = np_utils.to_categorical(y_train, n_classes)
Y_test = np_utils.to_categorical(y_test, n_classes)
print("Shape after one-hot encoding: ", Y_train.shape)

# building a linear stack of layers with the sequential model
model = Sequential()
# convolutional layer
model.add(Conv2D(64, kernel_size=(4,4), strides=(1,1), activation='relu', input_shape=(x,y,3)))
model.add(Dropout(.2))
model.add(BatchNormalization())

model.add(Conv2D(32, kernel_size=(4,4), strides=(1,1), activation='relu', input_shape=(x,y,3)))
model.add(Dropout(.2))
model.add(MaxPooling2D(pool_size=(2,2)))

# flatten output of conv
model.add(Flatten())
# hidden layer
model.add(Dense(48, activation='relu'))
model.add(Dropout(.2))

# output layer
model.add(Dense(2, activation='softmax'))

# compiling the sequential model
model.compile(loss='binary_crossentropy', metrics=['binary_accuracy'], optimizer='adam')


# In[6]:

model_name = sys.argv[1] if len(sys.argv) >= 2 else "mask-detector.h5"
model.load_weights("models/" + model_name)


# In[7]:


from os import walk
import glob, os

os.chdir("people/")
files = os.listdir()
os.chdir("../")


# In[8]:


dates = []

for file in files:
    date = file[:4] + "/" + file[4:6] + "/" + file[6:]
    dates.append(date)


# In[9]:


ppl_byday = []

ppl = []

for c, file in enumerate(files):

    #TODO: take all
    for i in range(3000):
        
        try:

            ppl.append([])

            img = Image.open("people/" +file + "/p-{}-{:06d}.jpg".format(file, i+1))
            width, height = img.size

            left = width/4
            top = 0
            right = 3*width/4
            bottom = height/2
            crp = img.crop((left, top, right, bottom)).resize((x,y))

            ppl[c].append(np.array(crp))

        except:
            continue
    ppl[c] = np.array(ppl[c])


# In[10]:


avg_daily = []

for i in range(len(files)):
    prediction_array = model.predict(ppl[i])
    prediction = np.argmax(prediction_array, axis=1)
    average    = np.average(prediction)
    avg_daily.append(average)


# In[18]:


plt.plot(np.array(avg_daily)*100)

# Fake dataset
ys = [0, 25, 50, 75, 100]
x_pos = np.arange(len(dates))
 

# Add title and axis names
plt.title('Percentage of mask wearers on İstiklâl St.')
plt.xlabel('Dates')
plt.ylabel('Mask usage (%)')

# Create names
plt.xticks(x_pos, dates)

plt.savefig("outputs/mask-usage-until-{}.png".format(files[-1]))

plt.show()

print(avg_daily)


# In[ ]:





# In[ ]:




