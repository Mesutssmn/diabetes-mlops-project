import sys
import os
from pathlib import Path


# Path setting: to find the src folder
sys.path.append(os.getcwd())

from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

def main():
    config_path = Path("configs/config.yaml")
    schema_path = Path("configs/schema.yaml")

    print("--- 1. DATA INGESTION ---")
    ingestion = DataIngestion(config_path)
    ingestion.initiate_data_ingestion()

    print("--- 2. DATA VALIDATION ---")
    validation = DataValidation(config_path, schema_path)
    if not validation.validate_all_columns():
        print("❌ Data validation failed!")
        return

    print("--- 3. DATA TRANSFORMATION ---")
    transformation = DataTransformation(config_path)
    X_train, X_test, y_train, y_test = transformation.initiate_data_transformation()

    print("--- 4. MODEL TRAINING ---")
    trainer = ModelTrainer(config_path)
    # Passing the data returned from Transformation to Trainer:
    trainer.initiate_model_trainer(X_train, X_test, y_train, y_test)
    
    print("✅ Pipeline completed successfully! Check MLflow UI.")

if __name__ == "__main__":
    main()