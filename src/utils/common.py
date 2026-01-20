import os
import yaml
import joblib
from pathlib import Path

def read_yaml(path_to_yaml: Path):
    """
    Reads a YAML file and returns it as a dictionary.
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            return content
    except Exception as e:
        raise e

def create_directories(path_to_directories: list, verbose=True):
    """
    Creates all directories (folders) in the given list.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            print(f"created directory at: {path}")

def save_object(file_path, obj):
    """
    Saves a Python object (model, scaler, etc.) to the specified path.
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        
        with open(file_path, "wb") as file_obj:
            joblib.dump(obj, file_obj)
            
    except Exception as e:
        raise e

def load_object(file_path):
    """
    Loads a Python object (model, scaler, etc.) from the specified path.
    """
    try:
        with open(file_path, "rb") as file_obj:
            return joblib.load(file_obj)
    except Exception as e:
        raise e