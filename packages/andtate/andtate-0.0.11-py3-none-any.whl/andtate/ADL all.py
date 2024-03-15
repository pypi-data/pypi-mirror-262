################### Implement Feed-forward Neural Network and train the network with different 
optimizers and compare the results. ###################
################### P1 ############################################################################


import tensorflow as tf
from tensorflow.keras import datasets, layers, models
# Load data
(train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data() 
print(train_images.shape)
print(train_labels.shape) 
print(test_images.shape) 
print(test_labels.shape)
# Normalize pixel values - betweem 0 and 1
train_images, test_images = train_images / 255.0, test_images / 255.0
------------------RUN------------------------------------------------------------------------
# Creating CNN model 
model = tf.keras.Sequential()
model.add(tf.keras.layers.Flatten(input_shape=(28, 28))) # or as a list 
model.add(tf.keras.layers.Dense(units=1000, activation=tf.keras.activations.sigmoid)) 
model.add(tf.keras.layers.Dense(units=10, activation=tf.keras.activations.softmax))
model.summary()
------------------RUN------------------------------------------------------------------------
# Compile 
model.compile(optimizer='adam',
loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), metrics=['accuracy'])
model.fit(train_images, train_labels, epochs=10, 
validation_data=(test_images, test_labels))



################### Write a program to implement regularization to prevent the model from 
overfitting. ###################
################### P2 ############################################################################


import numpy as np
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
lasso.fit(x_train, y_train)
------------------RUN------------------------------------------------------------------------
print("Lasso Train RMSE: ", 
np.round(np.sqrt(metrics.mean_squared_error(y_train,lasso.predict(x_train))),5))
------------------RUN------------------------------------------------------------------------
print("Lasso Train RMSE: ", 
np.round(np.sqrt(metrics.mean_squared_error(y_test,lasso.predict(x_test))),5))
------------------RUN------------------------------------------------------------------------
ridge = Ridge()
ridge.fit(x_train, y_train)
------------------RUN------------------------------------------------------------------------
print("Ridge Train RMSE: ", 
np.round(np.sqrt(metrics.mean_squared_error(y_train,ridge.predict(x_train))),5))
------------------RUN------------------------------------------------------------------------
print("Ridge Train RMSE: ", 
np.round(np.sqrt(metrics.mean_squared_error(y_test,ridge.predict(x_test))),5))


################### Implement deep learning for recognizing classes for datasets like CIFAR-10 
images for previously unseen images and assign them to one of the 10 classes. ###################
################### P3 ############################################################################

!pip install classes
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
classes[y_classes[4]]

################### Implement deep learning for the Prediction of the autoencoder from the test data. ###################
################### P4 ############################################################################

from tensorflow.keras.datasets import mnist
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
Dense(64, input_shape = (LATENT_SIZE,)),
LR(),
Dropout(0.5),
Dense(128),
LR(),
Dropout(0.5),
Dense(256),
LR(),
Dropout(0.5),
Dense(512),
LR(),
Dropout(0.5),
Dense(784),
Activation("sigmoid"),
Reshape((28, 28))
])

img = Input(shape = (28, 28))
latent_vector = encoder(img)
output = decoder(latent_vector)
model = Model(inputs = img, outputs = output)
model.compile("nadam", loss = "binary_crossentropy")
EPOCHS = 100
#Only do plotting if you have IPython, Jupyter, or using Colab
for epoch in range(EPOCHS):
 fig, axs = plt.subplots(4, 4, figsize=(4,4))
 rand = x_test[np.random.randint(0, 10000, 16)].reshape((4, 4, 1, 28, 28))
display.clear_output()
------------------RUN------------------------------------------------------------------------
for i in range(4):
 for j in range(4):
  axs[i, j].imshow(model.predict(rand[i, j])[0], cmap = "gray")
  axs[i, j].axis("off")
------------------RUN------------------------------------------------------------------------
plt.subplots_adjust(wspace = 0, hspace = 0)
plt.show()
print("-----------", "EPOCH", epoch, "-----------")
model.fit(x_train, x_train, batch_size = 64)


################### Implement Convolutional Neural Network for Digit Recognition on the 
MNIST Dataset. ###################
################### P5 ############################################################################

from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense,Conv2D,Flatten
import matplotlib.pyplot as plt
(X_train,Y_train),(X_test,Y_test)= mnist.load_data()
------------------RUN------------------------------------------------------------------------
plt.imshow(X_train[0])
plt.show()
------------------RUN------------------------------------------------------------------------
plt.imshow(X_train[1])
plt.show()
------------------RUN------------------------------------------------------------------------
print(X_train[0].shape)
X_train = X_train.reshape(60000,28,28,1)
X_test = X_test.reshape(10000,28,28,1)
------------------RUN------------------------------------------------------------------------
Y_train=to_categorical(Y_train)
Y_test=to_categorical(Y_test)
print(Y_train[0])
------------------RUN------------------------------------------------------------------------
model=Sequential()
model.add(Conv2D(64,kernel_size=3,activation='relu',input_shape=(28,28,1)))
model.add(Conv2D(32,kernel_size=3,activation='relu'))
model.add(Flatten())
model.add(Dense(10,activation='softmax'))
model=Sequential()
model.add(Conv2D(64,kernel_size=3,activation='relu',input_shape=(28,28,1)))
model.add(Conv2D(32,kernel_size=3,activation='relu'))
model.add(Flatten())
model.add(Dense(10,activation='softmax'))
model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=
['accuracy'])
model.fit(X_train,Y_train,validation_data=(X_test,Y_test),epochs=3)
------------------RUN------------------------------------------------------------------------
print(Y_test[:4])

################### Write a program to implement Transfer Learning on the suitable dataset (e.g. classify the cats versus dogs dataset from Kaggle).###################
################### P6 ############################################################################


import tensorflow as tf
import os
URL = 'https://storage.googleapis.com/mledu-datasets/cats_and_dogs_filtered.zip'
path_to_zip = tf.keras.utils.get_file('cats_and_dogs.zip', origin=URL, extract=True)
PATH = os.path.join(os.path.dirname(path_to_zip), 'cats_and_dogs_filtered')
------------------RUN------------------------------------------------------------------------
from tensorflow.keras.preprocessing import image_dataset_from_directory
train_dir = os.path.join(PATH, 'train')
validation_dir = os.path.join(PATH, 'validation')

BATCH_SIZE = 32
IMG_SIZE = (160, 160)
train_dataset = image_dataset_from_directory(train_dir, shuffle=True, batch_size=BATCH_SIZE, 
image_size=IMG_SIZE)
------------------RUN------------------------------------------------------------------------
validation_dataset = image_dataset_from_directory(validation_dir, shuffle=True, 
batch_size=BATCH_SIZE, image_size=IMG_SIZE)
------------------RUN------------------------------------------------------------------------
valdation_batches = tf.data.experimental.cardinality(validation_dataset)
print('Number of validation batches: %d' % tf.data.experimental.cardinality(validation_dataset))
test_batches = valdation_batches // 5
test_dataset = validation_dataset.take(test_batches)
print('Number of test batches: %d' % tf.data.experimental.cardinality(test_dataset))
validation_dataset = validation_dataset.skip(test_batches)
------------------RUN------------------------------------------------------------------------
class_names = train_dataset.class_names
class_names


###################  (4-to-1 RNN) to show that the quantity of rain on a certain day also 
depends on the values of the previous day ###################
################### P7 ############################################################################

import numpy as np
import tensorflow as tf
rainfall_data = np.array([[0.2, 0.3, 0.1, 0.5, 0.4],
[0.1, 0.4, 0.5, 0.2, 0.3],
[0.3, 0.2, 0.4, 0.3, 0.1],
[0.4, 0.1, 0.3, 0.4, 0.2],
[0.5, 0.5, 0.2, 0.1, 0.5]])
input_data = rainfall_data[:,:-1]
output_data = rainfall_data[:, -1]
model = tf.keras.Sequential([
tf.keras.layers.SimpleRNN(10, input_shape=(4, 1)),
tf.keras.layers.Dense(1)
])
model.compile(loss='mse', optimizer='adam')
model.fit(np.expand_dims(input_data, axis=2), output_data, epochs=100, batch_size=1)
------------------RUN------------------------------------------------------------------------
new_input = np.array([[0.3, 0.2, 0.1, 0.4]])
predicted_rainfall = model.predict(np.expand_dims(new_input, axis=2))
print("Predicted rainfall for the new day:", predicted_rainfall[0][0])

###################   Write a program for object detection from the image/video. ###################
################### P8 ############################################################################
!pip install torchvision
import torch
import torchvision
import torchvision.transforms as transforms
import pycocotools
from PIL import Image
from pycocotools.coco import COCO
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from torchvision.utils import draw_bounding_boxes

holiday = Image.open("kids.jpg").convert('RGB')
holiday

kids_playing = Image.open("kids.jpg").convert('RGB')
kids_playing

#holiday_tensor_int = PIL_to_tensor(holiday)
#kids_playing_tensor_int = PIL_to_tensor(kids_playing)

holiday_tensor_int = transforms.PILToTensor()(holiday)
kids_playing_tensor_int = transforms.PILToTensor()(kids_playing)
holiday_tensor_int.shape
kids_playing_tensor_int.shape

holiday_tensor_int = holiday_tensor_int.unsqueeze(dim=0)
kids_playing_tensor_int = kids_playing_tensor_int.unsqueeze(dim=0)
holiday_tensor_int.shape, kids_playing_tensor_int.shape

print(holiday_tensor_int.min(), holiday_tensor_int.max())

holiday_tensor_float = holiday_tensor_int / 255.0
kids_playing_tensor_float = kids_playing_tensor_int / 255.0
print(holiday_tensor_float.min(), holiday_tensor_float.max())

object_detection_model = fasterrcnn_resnet50_fpn(pretrained=True, progress=False)
object_detection_model.eval();
holiday_preds = object_detection_model(holiday_tensor_float)
holiday_preds

holiday_preds[0]["boxes"] = holiday_preds[0]["boxes"][holiday_preds[0]["scores"] > 0.8]
holiday_preds[0]["labels"] = holiday_preds[0]["labels"][holiday_preds[0]["scores"] > 0.8]
holiday_preds[0]["scores"] = holiday_preds[0]["scores"][holiday_preds[0]["scores"] > 0.8]
holiday_preds

kids_preds = object_detection_model(kids_playing_tensor_float)
kids_preds

#from pycocotools.coco import COCO
!wget https://huggingface.co/datasets/merve/coco/resolve/main/annotations/instances_val2017.json?download=true
!mv instances_val2017.json?download=true instances_val2017.json
annFile='/content/instances_val2017.json'
coco=COCO(annFile)
holiday_labels = coco.loadCats(holiday_preds[0]["labels"].numpy())
holiday_labels

kids_labels = coco.loadCats(kids_preds[0]["labels"].numpy())
kids_labels

holiday_annot_labels = ["{}-{:.2f}".format(label["name"], prob) for label, prob in zip(holiday_labels, holiday_preds[0]["scores"].detach().numpy())]
holiday_output = draw_bounding_boxes(image=holiday_tensor_int[0],
                                     boxes=holiday_preds[0]["boxes"],
                                     labels=holiday_annot_labels,
                                     colors=["red" if label["name"]=="person" else "green" for label in holiday_labels],
                                     width=2
)
holiday_output.shape


###################   Write a program for object detection using pre-trained models to use object 
detection. ###################
################### P9 ############################################################################

!wget https://github.com/AlexeyAB/darknet/blob/master/cfg/yolov3.cfg?raw=true -O yolov3.cfg
!wget https://pjreddie.com/media/files/yolov3.weights
------------------RUN------------------------------------------------------------------------
import cv2
import numpy as np
import urllib.request
import matplotlib.pyplot as plt
import tensorflow as tf
url = 'https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names'
urllib.request.urlretrieve(url, 'coco.names')
------------------RUN------------------------------------------------------------------------
model = tf.keras.applications.EfficientNetB0(include_top=False, weights='imagenet')
model.trainable = False
------------------RUN------------------------------------------------------------------------
obj_detector = cv2.dnn.readNetFromDarknet('yolov3.cfg', 'yolov3.weights')
obj_detector.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
obj_detector.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

def detect_objects(image):
 blob = cv2.dnn.blobFromImage(image, 1/255, (416, 416), swapRB=True, crop=False)
 obj_detector.setInput(blob)
 detections = obj_detector.forward()
 for detection in detections:
   scores = detection[5:]
   class_id = np.argmax(scores)
   confidence = scores[class_id]
   if confidence > 0.5:
    center_x = int(detection[0] * image.shape[1])
    center_y = int(detection[1] * image.shape[0])
    width = int(detection[2] * image.shape[1])
    height = int(detection[3] * image.shape[0])
    left = int(center_x - width/2)
    top = int(center_y - height/2)
    cv2.rectangle(image, (left, top), (left+width, top+height), (0, 255, 0), 2)
    cv2.putText(image, f'{class_id}', (left, top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,
255, 0), 2)
 return image

url = 'https://images.unsplash.com/photo-1594028411108-96a5b0302a4a?ixlib=rb4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80'
urllib.request.urlretrieve(url, 'example.jpg')
------------------RUN------------------------------------------------------------------------
image = cv2.imread('example.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image = detect_objects(image)
plt.imshow(image)
plt.axis('off')
plt.show()