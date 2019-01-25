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
from keras.layers.normalization import BatchNormalization
from keras.layers import Activation
from keras.layers import Dropout
from keras.optimizers import Adam
from sklearn.metrics import roc_auc_score

class Classifier:
    def __init__(self, input_size, epoch=30):
        self.input_size = input_size
        self.epoch = epoch
        self.model = self._model()

    def _model(self):
        model = Sequential()
        model.add(Dense(units=64, input_dim=self.input_size))
        model.add(BatchNormalization())
        model.add(Activation("relu"))
        model.add(Dropout(0.5))

        model.add(Dense(units=32))
        model.add(BatchNormalization())
        model.add(Activation("relu"))
        model.add(Dropout(0.5))

        model.add(Dense(units=1, activation="sigmoid"))

        model.compile(loss="mse", optimizer=Adam(lr=0.001))

        return model

    def fit(self, X, y, batch_size):
        self.model.fit(X,y,batch_size=batch_size,epochs=self.epoch)

    def predict(self, X):
        return self.model.predict(X)

    def evaluate(self, X, y):
        y_pred = self.model.predict(X,verbose=1)
        return roc_auc_score(y, y_pred)