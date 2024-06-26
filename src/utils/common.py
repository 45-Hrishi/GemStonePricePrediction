from sklearn.metrics import r2_score
from exception.exception import customexception
import pickle
import os
import sys
from logger.logger import logging
from box.exceptions import BoxValueError
import yaml
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
import pandas as pd

@ensure_annotations
def save_object(file_path,obj):
    try:
        logging.info(f"saving model at {file_path}")
        #getting the name of directory from file_path and then create it.
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        
        with open(file_path,'wb') as file_obj:
            pickle.dump(obj,file_obj)
        logging.info("model saved successfully")
    except Exception as e:
        raise customexception(e,sys)

@ensure_annotations
def evaluate_model(X_train,y_train,X_test,y_test,models:dict):
    # print(models)
    try:
        logging.info("Model selection started")
        report = {}

        for i in range(len(models)):
            logging.info(f"Model {list(models.keys())[i]} started")
            model = list(models.values())[i]
            model_obj = model.fit(X_train,y_train)

            y_pred = model_obj.predict(X_test)
            #evaluation of model
            score = r2_score(y_test,y_pred)
            report[model] = (score)
            logging.info(f"Model {list(models.keys())[i]} has the accuracy of {score}")
        return report
            
    except Exception as e:
        logging.info("Exception occured while evaluating model")
        raise customexception(e,sys)  

@ensure_annotations
def read_yaml(path_to_yaml):
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logging.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("YAML file is empty")
    
    except Exception as e:
        raise customexception(e,sys)

@ensure_annotations
def read_csv(path_to_csv):
    try:
        df = pd.read_csv(path_to_csv)
        logging.info(f"{path_to_csv} file read successfully")
        return df
    except Exception as e:
        raise customexception(e,sys)

@ensure_annotations
def get_transform_data(path_to_folder):
    train_transform = pd.read_csv(os.path.join(path_to_folder,"transform_train.csv")) 
    test_transform = pd.read_csv(os.path.join(path_to_folder,"transform_test.csv")) 
    
    X_train = train_transform.drop('price',axis=1)
    y_train = train_transform['price']
    
    X_test = test_transform.drop('price',axis=1)
    y_test = test_transform['price']
    
    return X_train,y_train,X_test,y_test
    
    

@ensure_annotations
def create_directories(directories_path:list,verbose=True):
    for path in directories_path:
        os.makedirs(path,exist_ok=True)
        if verbose:
            logging.info(f"Directory creted at : {path}")

@ensure_annotations
def save_json(path:Path,data:dict):
    with open(path,"w") as f:
        json.dump(data,f,indent=4)
    logging.info(f"Json file created at : {path}")

@ensure_annotations
def load_json(path:Path) -> ConfigBox:
    with open(path) as f:
        content = json.load(f)
    logging.info(f"JSON file loaded successfully")
    return ConfigBox(content)

@ensure_annotations
def get_size(path:Path):
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"{size_in_kb} KB"


@ensure_annotations    
def load_object(file_path):
    try:
        with open(file_path,'rb') as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        logging.info("Exception occured in load_object function")
        raise customexception(e,sys)