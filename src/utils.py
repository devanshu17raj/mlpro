import os
import sys
import dill # You might be using dill if you saved complex sklearn pipelines
import pickle # Standard Python module for serialization
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

from src.exception import CustomException

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            # Using pickle here as per your provided code
            pickle.dump(obj, file_obj)
    except Exception as e:
        raise CustomException(e, sys)
    
def evaluate_models(X_train, y_train,X_test,y_test,models,param):
    try:
        report = {}
        for i in range(len(list(models))):
            model = list(models.values())[i]
            para=param[list(models.keys())[i]]
            gs = GridSearchCV(model,para,cv=3)
            gs.fit(X_train,y_train)
            model.set_params(**gs.best_params_)
            model.fit(X_train,y_train)
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)
            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)
            report[list(models.keys())[i]] = test_model_score
        return report
    except Exception as e:
        raise CustomException(e, sys)
    
def load_object(file_path):
    try:
        # Debug print: Confirming path before opening
        print(f"DEBUG (load_object): Attempting to load object from: {file_path}")
        if not os.path.exists(file_path):
            print(f"DEBUG (load_object): File does NOT exist at: {file_path}")
            raise FileNotFoundError(f"Object file not found at {file_path}")

        with open(file_path, "rb") as file_obj:
            loaded_obj = pickle.load(file_obj)
            # Debug print: Confirming successful load
            print(f"DEBUG (load_object): Successfully loaded object from: {file_path}")
            return loaded_obj

    except Exception as e:
        # This will now print the specific error from inside load_object
        print(f"DEBUG (load_object): Error loading object from {file_path}: {e}")
        raise CustomException(e, sys)