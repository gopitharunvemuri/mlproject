import numpy as np
import pickle
import os
import sys
from src.exception import CustomException
from sklearn.metrics import r2_score
from src.logger import logging

def save_object(filepath, obj):
    try:
        dirname = os.path.dirname(filepath)
        os.makedirs(dirname, exist_ok=True)
        with open(filepath, "wb") as f:
            pickle.dump(obj, f)
    except Exception as e:
        raise CustomException(e, sys)
    
def evaluate_model(X_train, X_test, y_train, y_test, models):
    try:
        model_report = {}

        for i in models.items():
            d = {}
            model = i[1]
            name = i[0]
            model.fit(X_train, y_train)
            logging.info(f"The model is {name}")
            logging.info(f"The model is {model}")
            y_pred = model.predict(X_test)
            score = r2_score(y_pred = y_pred, y_true=y_test)
            model_report[name] = score

        return model_report
    except Exception as e:
        raise CustomException(e, sys)