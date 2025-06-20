import os
import sys

import numpy as np
import pandas as pd

from dataclasses import dataclass

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

from src.logger import logging
from src.exception import customException


from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessing_obj_file_path = os.path.join('artifacts',"preprocessing.pkl")


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformation_obj(self):
        try:
            numerical_columns =['reading_score', 'writing_score']
            categorical_columns =['gender', 'race_ethnicity', 'parental_level_of_education', 'lunch', 'test_preparation_course']

            num_pipeline = Pipeline(
                steps = [
                    ("imputer",SimpleImputer(strategy="median")),
                    ("scaler",StandardScaler(with_mean=False))
                ]
            )

            cat_pipeline = Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder",OneHotEncoder()),
                    ("scaler",StandardScaler(with_mean=False))
                ]
            )

            logging.info(f"categorical columns {categorical_columns}")
            logging.info(f"numerical_columns {numerical_columns}")


            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline",num_pipeline,numerical_columns),
                    ("cat_pipeline",cat_pipeline,categorical_columns)
                ]

            )

            return preprocessor
        
        except Exception as e:
            raise customException(e,sys)
        
    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("load read train test files")

            logging.info("obtaining data transformer object")

            preprocessing_obj = self.get_data_transformation_obj()

            target_column_name = ['math_score']
            numerical_columns = ['reading_score', 'writing_score']

            input_feature_train_df = train_df.drop(columns=target_column_name,axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=target_column_name,axis=1)
            target_feature_test_df = test_df[target_column_name]

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr,np.array(target_feature_test_df)]

            save_object (
                file_path = self.data_transformation_config.preprocessing_obj_file_path,
                obj = preprocessing_obj
            )

            logging.info("saved preprocessing object")

            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessing_obj_file_path,
            )
            
        except Exception as e:
            raise customException(e,sys)

