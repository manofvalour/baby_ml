import os
import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from xgboost import XGBRegressor
from catboost import CatBoostRegressor
from sklearn.metrics import r2_score

from src.logger import logging
from src.exception import CustomException
from src.utils import save_obj, evaluate_model


@dataclass
class ModelTrainingConfig():
    model_training_path= os.path.join('artifact', 'model.pkl')

class ModelTrain():
    def __init__(self):
        self.model_train_config= ModelTrainingConfig()

    def initiate_model_training(self, train_array, test_array):
        try:
            logging.info('splitting the train and test data')

            X_train, y_train, X_test, y_test= (
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )

            logging.info('Dataset splitted')

            logging.info('initiating models for training and evaluation')
            models={
                'linearReg': LinearRegression(),
                'Lasso': Lasso(),
                'Ridge': Ridge(),
                'SVR': SVR(),
                'RandomForest': RandomForestRegressor(),
                'GradientBoosting': GradientBoostingRegressor(),
                'AdaBoost': AdaBoostRegressor(),
                'DecisionTree': DecisionTreeRegressor(),
                'KNNRegressor': KNeighborsRegressor(),
                'XGBRegressor': XGBRegressor(),
                'CatBoostRegressor': CatBoostRegressor()
            }
            
            logging.info('models initiated')

            params = {
                "Decision Tree": {
                    
                }
            }


            model_report:dict= evaluate_model(X_train,y_train, 
                                              X_test,y_test,models)
                  
            
            logging.info('model trained')
            
            best_model_score= max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            best_model= models[best_model_name]

            logging.info('best model selected')

            if best_model_score<0.6:
                raise CustomException ('Best model not found!')
            logging.info('Best model for Training and Testing Data found')

            save_obj(file_path=self.model_train_config.model_training_path, obj=best_model)

            predicted = best_model.predict(X_test)
            r2score= r2_score(y_test, predicted)

            return r2score

        except Exception as e:
            CustomException(e, sys)