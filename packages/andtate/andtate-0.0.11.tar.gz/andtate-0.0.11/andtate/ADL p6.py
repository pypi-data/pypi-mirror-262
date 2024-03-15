
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

