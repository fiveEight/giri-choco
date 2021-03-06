# -*- coding: utf-8 -*-
"""giri-choco.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13YFby8kPyw0X5eUbRi6pM-RwqZR3763m
"""

from google.colab import drive
drive.mount("/content/drive/")

cd drive/My Drive/Colab Notebooks

pwd

# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

# Helper Libraries
import numpy as np
import matplotlib.pyplot as plt
import glob, os
import re

# Pillow
import PIL
from PIL import Image

# Use Pillow Library to Convert an Input JPEG to a 8-bit Grey Scale Image Array for Processing.
def jpeg_to_8_bit_greyscale(path, maxsize):
#     img = Image.open(path).convert('L') # Convert Image to 8-bit Grey Scale
    img = Image.open(path).convert('RGBA') # Convert Image to RGBA
    # Make Aspect Ratio as 1:1 by Applying Image Crop.
    # Please Note, Croping Works for this Data Set, but in General One
    # Needs to Locate the Subject and then Crop or Scale Accordingly.
    WIDTH, HEIGHT = img.size
    if WIDTH != HEIGHT:
        m_min_d = min(WIDTH, HEIGHT)
        img = img.crop((0,0,m_min_d,m_min_d))
    # Scale the Image to the Requested Max Size by Anti-alias Sampling.
    img.thumbnail(maxsize, PIL.Image.ANTIALIAS)
    return np.asarray(img)

def load_image_dataset(path_dir, maxsize):
    images = []
    labels = []
    os.chdir(path_dir)
    for file in glob.glob("*.jpg"):
        img = jpeg_to_8_bit_greyscale(file,maxsize)
        if re.match('honmei.*', file):
            images.append(img)
            labels.append(0)
        elif re.match('giri.*',file):
            images.append(img)
            labels.append(1)
    return (np.asarray(images), np.asarray(labels))

maxsize = 32,32

(train_images, train_labels) = load_image_dataset('/content/drive/My Drive/Colab Notebooks/honmei_giri2',maxsize)
(test_images, test_labels) = load_image_dataset('/content/drive/My Drive/Colab Notebooks/test_data',maxsize)

class_names = ['honmei', 'giri']

train_images.shape

print(train_labels)

test_images.shape

print(test_labels)

def display_images(images, labels):
    plt.figure(figsize = (10,10))
    grid_size = min(25, len(images))
    for i in range(grid_size):
        plt.subplot(5,5,i+1)
        plt.xticks([])
        plt.yticks([])
        plt.grid(False)
        plt.imshow(images[i],cmap=plt.cm.binary)
        plt.xlabel(class_names[labels[i]])

display_images(train_images, train_labels)
plt.show()

train_images = train_images / 255.0
test_images = test_images / 255.0

# Setting Up the Layers

model = keras.Sequential([
#     keras.layers.Flatten(input_shape=(100,100)),
    keras.layers.Flatten(input_shape=(32,32,4)),
        keras.layers.Dense(1024, activation=tf.nn.sigmoid),
        keras.layers.Dense(512, activation=tf.nn.sigmoid),
        keras.layers.Dense(128, activation=tf.nn.sigmoid),
        keras.layers.Dense(16, activation=tf.nn.sigmoid),
    keras.layers.Dense(2,activation=tf.nn.softmax)
])

sgd = keras.optimizers.SGD(lr=0.01, decay=1e-5, momentum=0.7, nesterov=True)

model.compile(optimizer=sgd,
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(train_images,train_labels,epochs=250)

test_loss, test_acc = model.evaluate(test_images, test_labels)
print('Test Accuracy: ', test_acc)
print('Test Loss: ', test_loss)

predictions = model.predict(test_images)

print(predictions)

display_images(test_images, np.argmax(predictions, axis = 1))
plt.show()

