'''################### Implement Feed-forward Neural Network and train the network with different 
optimizers and compare the results. ###################'''
'''################### P1 ############################################################################'''

'''import tensorflow as tf
from tensorflow.keras import datasets, layers, models
# Load data
(train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data() 
print(train_images.shape)
print(train_labels.shape) 
print(test_images.shape) 
print(test_labels.shape)
# Normalize pixel values - betweem 0 and 1
train_images, test_images = train_images / 255.0, test_images / 255.0'''
'''------------------RUN------------------------------------------------------------------------
# Creating CNN model 
model = tf.keras.Sequential()
model.add(tf.keras.layers.Flatten(input_shape=(28, 28))) # or as a list 
model.add(tf.keras.layers.Dense(units=1000, activation=tf.keras.activations.sigmoid)) 
model.add(tf.keras.layers.Dense(units=10, activation=tf.keras.activations.softmax))
model.summary()'''
'''------------------RUN------------------------------------------------------------------------
# Compile 
model.compile(optimizer='adam',
loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), metrics=['accuracy'])
model.fit(train_images, train_labels, epochs=10, 
validation_data=(test_images, test_labels))'''



'''################### Write a program to implement regularization to prevent the model from 
overfitting. ###################'''
'''################### P2 ############################################################################'''

'''import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge
df_train = pd.read_csv('train.csv')
df_test = pd.read_csv('test.csv')
df_train = df_train.dropna()
df_test = df_test.dropna()
x_train = df_train['x']
x_train = x_train.values.reshape(-1,1)
y_train = df_train['y']
y_train = y_train.values.reshape(-1,1)
x_test = df_test['x']
x_test = x_test.values.reshape(-1,1)
y_test = df_test['y']
y_test = y_test.values.reshape(-1,1)
lasso = Lasso()
lasso.fit(x_train, y_train)'''
'''------------------RUN------------------------------------------------------------------------
print("Lasso Train RMSE: ", 
np.round(np.sqrt(metrics.mean_squared_error(y_train,lasso.predict(x_train))),5))'''
'''------------------RUN------------------------------------------------------------------------
print("Lasso Train RMSE: ", 
np.round(np.sqrt(metrics.mean_squared_error(y_test,lasso.predict(x_test))),5))'''
'''------------------RUN------------------------------------------------------------------------
ridge = Ridge()
ridge.fit(x_train, y_train)'''
'''------------------RUN------------------------------------------------------------------------
print("Ridge Train RMSE: ", 
np.round(np.sqrt(metrics.mean_squared_error(y_train,ridge.predict(x_train))),5))'''
'''------------------RUN------------------------------------------------------------------------
print("Ridge Train RMSE: ", 
np.round(np.sqrt(metrics.mean_squared_error(y_test,ridge.predict(x_test))),5))'''


'''################### Implement deep learning for recognizing classes for datasets like CIFAR-10 
images for previously unseen images and assign them to one of the 10 classes. ###################'''
'''################### P3 ############################################################################'''

'''!pip install classes
import classes
import tensorflow as tf
from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report

(X_train, y_train), (X_test,y_test) = datasets.cifar10.load_data()

X_train.shape
X_test.shape
y_train.shape
y_test.shape
y_train = y_train.reshape(-1,)
y_train[:5]
y_test = y_test.reshape(-1,)

for i in range(9):
  plt.subplot(330 + 1 + i)
  plt.imshow(X_train[i])
plt.show()

for i in range(9):
  plt.subplot(330 + 1 + i)
  plt.imshow(X_train[i])
plt.show()

def plot_sample(x, y, index):
  plt.figure(figsize = (15,2))
  plt.imshow(x[index])
  plt.xlabel(classes [y[index]])

X_train = X_train / 255.0
X_test = X_test/255.0

ann = models.Sequential([
layers. Flatten (input_shape=(32,32,3)),
layers.Dense (3000, activation='relu'),
layers.Dense (1000, activation='relu'),
layers.Dense (10, activation='softmax')
])

ann.compile(optimizer='SGD',loss='sparse_categorical_crossentropy',metrics=['accuracy'])
ann.fit(X_train, y_train, epochs=10)

y_pred = ann.predict(X_test)
y_pred_classes = [np.argmax(element) for element in y_pred]
print("Classification Report: \n", classification_report(y_test, y_pred_classes))

cnn = models.Sequential([
layers.Conv2D(filters=32, kernel_size=(3, 3), activation='relu', input_shape=(32, 32, 3)),
layers.MaxPooling2D((2, 2)),
layers.Conv2D(filters=64, kernel_size=(3, 3), activation='relu'),
layers.MaxPooling2D((2, 2)),
layers.Flatten(),
layers.Dense(64, activation='relu'),
layers.Dense(10, activation='softmax')
])

cnn.compile(optimizer='adam',loss='sparse_categorical_crossentropy',metrics=['accuracy'])
cnn.fit(X_train, y_train, epochs=10)

cnn.evaluate(X_test,y_test)

y_pred = cnn.predict(X_test)

y_pred[:5]

y_classes = [np.argmax(element) for element in y_pred]
y_classes[:5]
y_test[:5]

classes = ["airplane","automobile","bird","cat","deer","dog","frog","horse","ship","truck"]

def plot_sample(x, y, index):
    plt.figure(figsize = (15,2))
    plt.imshow(x[index])
    plt.xlabel(classes[y[index]])

plot_sample(X_test, y_test,4)
#plt.xlabel(classes[y[index]])
classes[y_classes[4]]'''


'''################### Implement deep learning for the Prediction of the autoencoder from the test data. ###################'''
'''################### P4 ############################################################################'''

'''from tensorflow.keras.datasets import mnist
from tensorflow.keras.layers import Dense, Input, Flatten,Reshape,LeakyReLU as LR, Activation, Dropout
from tensorflow.keras.models import Model, Sequential
from matplotlib import pyplot as plt
from IPython import display
import numpy as np

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = x_train/255.0
x_test = x_test/255.0
# Plot image data from x_train
plt.imshow(x_train[0], cmap = "gray")
plt.show()
------------------RUN------------------------------------------------------------------------

LATENT_SIZE = 32
encoder = Sequential([
Flatten(input_shape = (28, 28)),
Dense(512),
LR(),
Dropout(0.5),
Dense(256),
LR(),
Dropout(0.5),
Dense(128),
LR(),
Dropout(0.5),
Dense(64),
LR(),
Dropout(0.5),
Dense(LATENT_SIZE, activation="sigmoid"),
])

decoder = Sequential([
Dense(64, input_shape = (
'''