
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

