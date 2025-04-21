
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
import os
import sys

from src.logger import logging
from src.exception import CustomException
from sklearn.pipeline import Pipeline
from src.utils import save_obj
from dataclasses import dataclass

@dataclass
class DataTransformationConfig:
    preprocessor_obj_filepath= os.path.join('artifact', 'preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config= DataTransformationConfig()

    def data_transformation_obj(self):
        '''this function is responsible for data transformation'''
        
        try:
            logging.info('setting up the data')
            num_columns = ['case', 'gestation', 'age', 
                          'height', 'weight']
            bool_column =['parity', 'smoke']
            
            logging.info('setting up the pipeline')

            int_pipeline = Pipeline(
                steps=[
                    ('SimpleImputer', SimpleImputer(strategy='median')),
                    ('scaler', StandardScaler())
                ]
            )

            cat_pipeline = Pipeline(
                steps=[
                    ('simple_impute', SimpleImputer(strategy='most_frequent')),
                    ('scaler', StandardScaler())
                ]
            )

            logging.info('pipeline setup completed')

            preprocessor= ColumnTransformer(
                [
                    ('int_pipeline', int_pipeline, num_columns),
                    ('bool_pipeline', cat_pipeline, bool_column)
                ]
            )

            logging.info('column transformation completed')


            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)
        

    def initiate_data_transformation(self, train_path, test_path):

        try:
            logging.info('importing the dataset')

            train_data= pd.read_csv(train_path)
            test_data= pd.read_csv(test_path)

            preprocessor_obj = self.data_transformation_obj()

            logging.info('data successfully imported')

            logging.info('spiltting the data into independent and target variables')

            target_column_name= 'bwt'

            train_independent_variables = train_data.drop(columns=[target_column_name], axis=1)
            train_dependent_variable = train_data[target_column_name]

            test_independent_variables= test_data.drop(columns=[target_column_name], axis=1)
            test_dependent_variable= test_data[target_column_name]

            logging.info('data has been successfully splitted')

            train_preprocessed = preprocessor_obj.fit_transform(train_independent_variables)
            test_preprocessed = preprocessor_obj.transform(test_independent_variables)

            logging.info('data has been successfully preprocessed')

            logging.info('saving the data into pkl file')

            train_arr= np.c_[train_preprocessed, np.array(train_dependent_variable)]
            test_arr= np.c_[test_preprocessed, np.array(test_dependent_variable)]

            logging.info('train_arr and test_arr are created')

            logging.info('saving the pkl file')

            save_obj(file_path=self.data_transformation_config.preprocessor_obj_filepath, 
                     obj=preprocessor_obj)
            
            logging.info('pkl file saved successfully')


            return (
                train_arr,
                test_arr,
                preprocessor_obj
            )
    
        except Exception as e:
            raise CustomException(e, sys)