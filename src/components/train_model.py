import os
import sys

from dataclasses import dataclass

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor

from sklearn.ensemble import(
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor
)

from catboost import CatBoostRegressor
from xgboost import XGBRFRegressor

from src.exception import customException
from src.logger import logging
from src.utils import save_object,evaluate_models

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts","model.pkl")


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self,train_array,test_array):

        try:
            logging.info("splitting Train and test data")
            X_train,y_train,X_test,y_test=(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1],
            )
            models ={
                "linear_regression":LinearRegression(),
                "k-Neighbors classifier":KNeighborsRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Ada Boost Regressor": AdaBoostRegressor(),
                "Gradient Boost Regressor":GradientBoostingRegressor(),
                "XGBRF Regressor":XGBRFRegressor(),
                "cat boost Regressor":CatBoostRegressor(verbose=False),
                "Random Forest":RandomForestRegressor(),

            }

            model_report: dict= evaluate_models(X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test,
                                               models=models)
            
            best_model_score =   max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
                ]
            
            best_model = models[best_model_name]

            if best_model_score<0.6:
                raise customException("best model not found")
            logging.info("Found best model on trained and test data")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj = best_model
            )

            predicted = best_model.predict(X_test)

            r2_square = r2_score(y_test,predicted)
            return r2_square


        except Exception as e:
            raise customException(e,sys)