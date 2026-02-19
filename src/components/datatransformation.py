import sys
import pandas as pd
import numpy as np
import os
from dataclasses import dataclass
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from src.utils import save_object

from src.logger import logging
from src.exception import CustomException

@dataclass
class DataTransformationConfig:
    preprocessing_pkl_object = os.path.join("artifacts", "preprocessing_obj")

class DataTransformation:
    def __init__(self):
        self.datatransformationconfig = DataTransformationConfig()

    def get_data_transformer_object(self, train_data):
        try:
            numerical_columns = []
            categorical_columns = []
            columns = train_data.columns
            for i in columns:
                if i == "math_score":
                    continue
                if train_data[i].dtype != "str":
                    numerical_columns.append(i)
                else:
                    categorical_columns.append(i)
                    
            numerical_pipeline = Pipeline(
                steps = [
                    ("impute", SimpleImputer(strategy = "median")),
                    ("scaler", StandardScaler())
                ]
            )    

            categorical_pipeline = Pipeline(
                steps = [
                    ("impute", SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder", OneHotEncoder()),
                    ("scaler", StandardScaler(with_mean = False))
                ]
            )
            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")

            preprocessor=ColumnTransformer(
                [
                ("num_pipeline",numerical_pipeline,numerical_columns),
                ("cat_pipelines",categorical_pipeline,categorical_columns)

                ]


            )
            return preprocessor
        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_datatarnsformation(self, train_path, test_path):
        try:
            train_data = pd.read_csv(train_path)
            test_data = pd.read_csv(test_path)
            
            logging.info("Read the data sets")
            logging.info("Getting the preprocessing object")
            preprocessor = self.get_data_transformer_object(train_data=train_data)

            target_column = "math_score"
            
            input_feature_train=train_data.drop(target_column, axis=1)
            target_feature_train = train_data[target_column]

            input_feature_test = test_data.drop(target_column, axis=1)
            target_feature_test = test_data[target_column]

            input_feature_train_arr = preprocessor.fit_transform(input_feature_train)
            input_feature_test_arr = preprocessor.transform(input_feature_test)

            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train)
            ]
            test_arr = np.c_[
                input_feature_test_arr, np.array(target_feature_test)
            ]

            logging.info(f"Saved preprocessing object.")

            save_object(

                filepath=self.datatransformationconfig.preprocessing_pkl_object,
                obj=preprocessor

            )

            return (
                train_arr,
                test_arr,
                self.datatransformationconfig.preprocessing_pkl_object,
            )
        except Exception as e:
            raise CustomException(e, sys)
