import numpy as np
import pickle
import os
import sys
from src.exception import CustomException

def save_object(filepath, obj):
    try:
        dirname = os.path.dirname(filepath)
        os.makedirs(dirname, exist_ok=True)
        with open(filepath, "wb") as f:
            pickle.dump(obj, f)
    except Exception as e:
        raise CustomException(e, sys)