import sys
import pandas as pd
from src.exception import CustomException
from src.utils import load_obj


class PredictPipeline:
    def __init__(self):
        pass

    def predict(self, features):
        try:
            model_path='artifact\model.pkl'
            preprocessor_path= 'artifact\preprocessor.pkl'

            model= load_obj(file_path=model_path)
            preprocessor= load_obj(file_path=preprocessor_path)

            data_scaled= preprocessor.transform(features)
            pred= model.predict(data_scaled)

            return pred

  
        except Exception as e:
            raise CustomException(e, sys)



class CustomData:
    def __init__(self,case:int,bwt:int,gestation:int,parity:int, 
                 age:int,height:int,weight:int,smoke:int):
        
        self.case = case
        self.bwt= bwt
        self.getation = gestation
        self.parity= parity
        self.age=age
        self.height=height
        self.weight=weight
        self.smoke=smoke

    def get_data_as_dataframe(self):
        try:
            custom_data_input_dict={
                'case':[self.gender],
                'btw':[self.btw],
                'gestation':[self.gestation],
                'parity':[self.parity],
                'age': [self.age],
                'height':[self.height],
                'weight':[self.weight],
                'smoke':[self.smoke]
            }

            return pd.DataFrame(custom_data_input_dict)
        
        except Exception as e:
            raise CustomException(e,sys)


        
