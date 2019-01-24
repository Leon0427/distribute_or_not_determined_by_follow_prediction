#coding:utf8
import keras
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense
from keras.optimizers import Adam
from ..config.global_config import PARENT_DATA_DIR
import os
from datetime import date as dt

import numpy as np
import random
from collections import deque

class Agent:
    def __init__(self, state_size, is_eval=False, model_name="",
                 gamma = 0.95,
                 epsilon = 1.0,
                 epsilon_min = 0.01,
                 epsilon_decay = 0.995):
        self.state_size = state_size
        self.action_size = 3
        self.memory = deque(max_len=1000)
        self.inventory = []
        self.model_name = model_name
        self.is_eval = is_eval

        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay

        self.model = load_model( os.path.join(PARENT_DATA_DIR,"rl_model/") + model_name) if is_eval else self._model()

    def _model(self):
        model = Sequential()
        model.add(Dense(units=64, input_dim=self.state_size, activation="relu"))
        model.add(Dense(units=32, activation="relu"))
        model.add(Dense(units=8, activation="relu"))
        model.add(Dense(units=self.action_size, activation="linear"))
        model.compile(loss="mse", optimizer=Adam(lr=0.001))

        return model

    def act(self, state):
        if not self.is_eval and random.random() <= self.epsilon:
            # not eval means in training, consider exploring
            # if is eval, no need to explore, just exploit
            return random.randrange(self.action_size)
        options = self.model.predict(state)
        return np.argmax(options[0])

    def expReplay(self, batch_size):
        mini_batch = []
        l = len(self.memory)
        for i in range(l - batch_size + 1, l):
            mini_batch.append(self.memory[i])
        states = np.zeros([batch_size, self.state_size])
        targets_f = np.zeros([batch_size, self.action_size])
        for i, (state, action, reward, next_state, done) in enumerate(mini_batch):
            # immediate_reward
            target = reward
            if not done:
                # expected_gain = immediate_reward + gamma * next_state_gain
                target += self.gamma * np.amax(self.model.predict(next_state)[0])
            target_f = self.model.predict(state) # model prediction
            target_f[0][action] = target # use expected_grain to as label
            targets_f[i] = target_f
            states[i] = state
        self.model.fit(states, targets_f, epochs=1, verbose=0)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay