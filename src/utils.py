import os
import sys
import dill

import pandas as pd
import numpy as np
from sklearn.metrics import r2_score

from sklearn.model_selection import GridSearchCV

from src.exception import CustomException


def save_obj(file_path, obj):
    '''for saving object into a file'''

    try:
        dir_path= os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, 'wb') as file_obj:
            dill.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)


def evaluate_model(X_train, y_train, X_test, y_test, models, params):

    try:

        report={}
        for i in range(len(list(models()))):
            model= list(models.values())[i]
            params= list(model.keys())[i]

            grid=GridSearchCV(estimator=model, param_grid=params)
            grid.fit(X_train, y_train)

            grid.set_params(**grid.best_params_)
            grid.fit(X_train,y_train)
            
            #model.fit(X_train, y_train) #training dataset
            
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            #result evaluation
            y_train_score=r2_score(y_train, y_train_pred)
            y_test_score= r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]]=y_test_score

        return report

    except Exception as e:
        raise CustomException(e,sys)


def load_obj(file_path):
    try:
        with open(file_path, 'rb') as file_obj:
            return dill.load(file_obj)
        
    except Exception as e:
        raise CustomException(e,sys)



    

