
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

