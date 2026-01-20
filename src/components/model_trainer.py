import pandas as pd
import numpy as np
from sklearn.linear_model import ElasticNet
import mlflow
import mlflow.sklearn
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from pathlib import Path
from src.utils.common import read_yaml
import os
os.environ['MLFLOW_HTTP_REQUEST_TIMEOUT'] = "10"

class ModelTrainer:
    def __init__(self, config_path: Path):
        self.config = read_yaml(config_path)

    def eval_metrics(self, actual, pred):
        rmse = np.sqrt(mean_squared_error(actual, pred))
        mae = mean_absolute_error(actual, pred)
        r2 = r2_score(actual, pred)
        return rmse, mae, r2

    def initiate_model_trainer(self, X_train, X_test, y_train, y_test):
        # MLflow ayarları
        mlflow.set_tracking_uri(self.config['mlflow']['tracking_uri'])
        mlflow.set_experiment(self.config['mlflow']['experiment_name'])

        with mlflow.start_run():
            # Create model (Parameters can also be taken from config)
            lr = ElasticNet(alpha=0.1, l1_ratio=0.5, random_state=42)
            lr.fit(X_train, y_train)

            # Predictions and Metrics
            predicted_qualities = lr.predict(X_test)
            (rmse, mae, r2) = self.eval_metrics(y_test, predicted_qualities)

            print(f"Elasticnet model (rmse={rmse}, mae={mae}, r2={r2})")

            # Log to MLflow
            mlflow.log_params({"alpha": 0.1, "l1_ratio": 0.5})
            mlflow.log_metric("rmse", rmse)
            mlflow.log_metric("r2", r2)
            mlflow.log_metric("mae", mae)

            # Save model to MLflow (for Model Registry)
            mlflow.sklearn.log_model(lr, "model", registered_model_name="DiabetesElasticNetModel")
            
            return lr

if __name__ == "__main__":
    try:
        config_path = Path("configs/config.yaml")
        trainer = ModelTrainer(config_path)
        
        # Read training and test data (saved in Transformation step)
        # Note: Ensure paths are compatible with config.yaml
        train_data = pd.read_csv("data/processed/train.csv")
        test_data = pd.read_csv("data/processed/test.csv")
        
        # Separate target variable from raw data (if target was not separated in Transformation)
        # In our scenario, the target variable is 'target'
        # If you deleted target in Transformation, you should read y_train and y_test separately
        
        # For simplicity, we simulate the outputs of the Transformation step:
        # (In a real scenario, the Transformation object would return these)
        X_train = train_data.drop(["target"], axis=1) if "target" in train_data.columns else train_data
        y_train = pd.read_csv("data/raw/diabetes.csv")['target'][:len(X_train)] # For example purposes
        
        # NOTE: The healthiest way is to call it through main.py, but 
        # if you want to run it alone, you should load the data from here.
        
        print("🚀 Model training is starting...")
        # IMPORTANT: initiate_model_trainer function expects parameters!
        # You should prepare X_train, X_test, y_train, y_test data above and give it here.
        
    except Exception as e:
        print(f"❌ Error occurred: {e}")