#%%
from keras.models import Sequential
from keras.layers.convolutional import Conv3D
from keras.layers.convolutional_recurrent import ConvLSTM2D
from keras.layers.normalization import BatchNormalization
import numpy as np
import pylab as plt
from keras import backend as K
import tensorflow as tf
import keras
print(tf.__version__)
print(keras.__version__)
#%%
