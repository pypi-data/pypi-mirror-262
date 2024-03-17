import pandas as pd
import numpy as np
import os
import pandas as pd
import time
import plotly.express as px
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import plot_model
from tensorflow import keras
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from keras.layers import Dense,BatchNormalization,Dropout
from keras.models import Sequential
from sklearn.model_selection import LeaveOneOut
import keras_tuner as kt
from keras.losses import MeanSquaredLogarithmicError
msle = MeanSquaredLogarithmicError()
import shutil



def binary_classification(X,Y,tst):
    xtrain,xtest,ytrain,ytest = train_test_split(X,Y, test_size=tst)
    def build_model(hp):
            shape = [xtrain.shape[1]]
            model = Sequential()
            model.add(Dense(16,input_shape=shape,activation='relu'))
            model.add(Dense(1,activation='sigmoid'))
            optimizer = hp.Choice('optimizer',['adam','adagrad','sgd','adadelta','rmsprop'])
            model.compile(optimizer=optimizer,loss='mean_squared_error',metrics=['accuracy'])
            return model

    tuner = kt.RandomSearch(build_model,objective='val_accuracy',max_trials=5)
    tuner.search(xtrain,ytrain,epochs=100,batch_size=10,validation_data=(xtest,ytest))
    models = tuner.get_best_models(num_models=2)
    return models[0]
    

def welcome():
    print("Welcome\n Hlo Coder i am R Kiran Kumar Reddy and i am the developer of this tuned classification. Use the docs for better experience.")

def reset():
    os.rmdir("untitled_project")

