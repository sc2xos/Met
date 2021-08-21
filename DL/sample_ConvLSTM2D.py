#%%
import numpy as np
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.models import Sequential
from keras.layers import LSTM, Dense, ConvLSTM2D
from keras.layers.convolutional import Conv3D
from keras.layers.normalization import BatchNormalization
import numpy as np
print(tf.__version__)
#%%
data_dim = 40
timesteps = 40
num_classes = 10
#%%
# Generate dummy training data
x_train = np.random.random((1200, 15, 40,40,1))
y_train = np.random.random((1200, 15, 40,40,1)) #x_train = x_train.reshape([-1,1,40, 40,1])
print(x_train.shape)
# Generate dummy validation data
x_val = np.random.random((100, timesteps, data_dim))
y_val = np.random.random((100, num_classes))
x_val = x_val.reshape([-1,1,40, 40,1])
#noisy_movies[:1000], shifted_movies[:1000], batch_size=10,epochs=300, validation_split=0.05
#%%
model = Sequential()
model.add(ConvLSTM2D(filters=40, kernel_size=(3, 3),
                   input_shape=(None, 40, 40, 1),
                   padding='same', return_sequences=True))
model.add(BatchNormalization())

model.add(ConvLSTM2D(filters=40, kernel_size=(3, 3),
                   padding='same', return_sequences=True))
model.add(BatchNormalization())

model.add(ConvLSTM2D(filters=40, kernel_size=(3, 3),
                   padding='same', return_sequences=True))
model.add(BatchNormalization())

model.add(ConvLSTM2D(filters=40, kernel_size=(3, 3),
                   padding='same', return_sequences=True))
model.add(BatchNormalization())

model.add(Conv3D(filters=1, kernel_size=(3, 3, 3),
               activation='sigmoid',
               padding='same', data_format='channels_last'))
model.compile(loss='binary_crossentropy', optimizer='adadelta')
#%%
model.fit(x_train[:1000], y_train[:1000],
          batch_size=10, epochs=10,
          validation_split=0.05)