import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
import os

from src.logger import logging
from src.exception import CustomException
from src.components.data_transformation import DataTransformation
import sys

@dataclass
class DataIngestionConfig:
        train_data_path:str = os.path.join('artifact', 'train_data.csv')
        test_data_path:str = os.path.join('artifact', 'test_data.csv')
        raw_data_path:str = os.path.join('artifact', 'raw_data.csv')


class DataIngestion:
    def __init__(self):
        self.ingestion_config= DataIngestionConfig()

    def initiate_data_ingestion(self):

        '''this method helps with importing dataset'''

        try:
            logging.info('Importing the dataset')
            df=pd.read_csv('notebook/data/babies.csv') #importing the dataset
            logging.info('Data has been imported')

            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True) #creating the directory
            logging.info('directory for storing the dataset has been made')


            logging.info('storing the imported data')
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True) #storing the imported data in csv

            logging.info('Splitting the dataset into train and test data')
            train_data, test_data= train_test_split(df, test_size=0.25, random_state=42) #splitting the data to train/test data

            logging.info('saving the splitted train and test data')
            train_data.to_csv(self.ingestion_config.train_data_path, index=False, header=True) #storing the train data
            test_data.to_csv(self.ingestion_config.test_data_path, index=False, header=True) #storing the test data

            logging.info('Successfully split and stored the imported data')

            return (self.ingestion_config.train_data_path, 
                    self.ingestion_config.test_data_path)   

        except Exception as e:
            CustomException(e, sys)
            
if __name__=="__main__":
    try:
        obj=DataIngestion()
        obj.initiate_data_ingestion()
        transform= DataTransformation()
        transform.initiate_data_transformation(train_path='artifact/train_data.csv', 
                                               test_path='artifact/test_data.csv')
     
    except Exception as e:
        raise CustomException(e, sys)
     