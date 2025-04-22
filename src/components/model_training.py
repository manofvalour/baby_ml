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

from src.logger import logging
from src.exception import CustomException
from src.utils import save_obj


@dataclass
class ModelTrainingConfig():
    model_training_path= os.path.join('artifact', 'model.pkl')

class ModelTrain():
    def __init__(self):
        self.model_train_config= ModelTrainingConfig()

    def initiate_model_training(self, train_data, test_data, preprocessor_path):
        
