
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

