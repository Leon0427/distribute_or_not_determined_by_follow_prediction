#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/25 16:40
# @Author  : liangxiao
# @Site    : 
# @File    : Classifier.py
# @Software: PyCharm
from keras.models import Model
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Input
from keras.layers.normalization import BatchNormalization
from keras.layers import Activation
from keras.layers import Dropout
from keras.optimizers import Adam
from keras import backend as K
from sklearn.metrics import roc_auc_score
import numpy as np
from keras.layers import Flatten, Lambda,  Add
from keras import layers

class DCNClassifier:
    def __init__(self, input_size, batch_size = 512, epoch=30):
        self.input_size = input_size
        self.epoch = epoch
        self.batch_size = batch_size
        self.model = self._model()

    def _model(self):
        # --- start with deep neural net work
        input = Input(batch_shape=[self.batch_size,self.input_size])
        x1 = Dense(units=64,input_shape=[self.batch_size,self.input_size])(input)
        x1_batch = BatchNormalization()(x1)
        x1_act = Activation("relu")(x1_batch)
        x1_drop = Dropout(0.5)(x1_act)

        x2 = Dense(units=32)(x1_drop)
        x2_batch = BatchNormalization()(x2)
        x2_act = Activation("relu")(x2_batch)
        x2_drop = Dropout(0.5)(x2_act)

        # ---- cross network
        cross_input = K.reshape(input, (self.batch_size,1,self.input_size))
        print cross_input,"====="
        cross = CrossLayer(output_dim=cross_input.shape[2], num_layer=3, name="cross_layer")(cross_input)
        cross = K.reshape(cross,(self.batch_size, self.input_size))
        print x2_drop.shape,">>>>"
        print cross.shape,"<<<"

        concatenated = K.concatenate([x2_drop, cross])

        out = Dense(units=1, activation="sigmoid")(concatenated)
        model = Model(inputs=[input], outputs=out)



        # model = Sequential()
        # model.add(Dense(units=64, input_dim=self.input_size))
        # model.add(BatchNormalization())
        # model.add(Activation("relu"))
        # model.add(Dropout(0.5))
        #
        # model.add(Dense(units=32))
        # model.add(BatchNormalization())
        # model.add(Activation("relu"))
        # model.add(Dropout(0.5))
        #
        # model.add(Dense(units=1, activation="sigmoid"))

        model.compile(loss="mse", optimizer=Adam(lr=0.001))

        return model

    def fit(self, X, y):
        self.model.fit(X,y,batch_size=self.batch_size,epochs=self.epoch)

    def predict(self, X):
        return self.model.predict(X)

    def evaluate(self, X, y):
        y_pred = self.model.predict(X,verbose=1)
        return roc_auc_score(y, y_pred)

class CrossLayer(layers.Layer):
    def __init__(self, output_dim, num_layer, **kwargs):
        self.output_dim = output_dim
        self.num_layer = num_layer
        super(CrossLayer, self).__init__(**kwargs)

    def build(self, input_shape):
        print input_shape
        self.input_dim = input_shape[2]
        self.W = []
        self.bias = []
        for i in range(self.num_layer):
            self.W.append(self.add_weight(shape = [1, self.input_dim], initializer = 'glorot_uniform', name = 'w_' + str(i), trainable = True))
            self.bias.append(self.add_weight(shape = [1, self.input_dim], initializer = 'zeros', name = 'b_' + str(i), trainable = True))
        self.built = True

    def call(self, input):
        for i in range(self.num_layer):
            if i == 0:
                constant = np.eye(input.shape[2])
                constant = np.repeat(constant[np.newaxis, ...],input.shape[0],axis=0)
                print "constant shape: %s" % str(constant.shape)
                print "bias shape %s" % self.bias[0].shape
                print self.bias[i] * Input(tensor=K.constant(constant))
                print (self.W[i] * K.batch_dot(K.reshape(input, (-1, self.input_dim, 1)), input)).shape
                cross = Lambda(lambda x: Add()([K.sum(self.W[i] * K.batch_dot(K.reshape(x, (-1, self.input_dim, 1)), x), 1, keepdims = True),  K.reshape(K.repeat(self.bias[i],input.shape[0]),input.shape), x]))(input)
            else:
                cross = Lambda(lambda x: Add()([K.sum(self.W[i] * K.batch_dot(K.reshape(x, (-1, self.input_dim, 1)), input), 1, keepdims = True), K.reshape(K.repeat(self.bias[i],input.shape[0]),input.shape), input]))(cross)
        return Flatten()(cross)

    def compute_output_shape(self, input_shape):
        return (None, self.output_dim)