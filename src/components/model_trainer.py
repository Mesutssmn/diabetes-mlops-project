import pandas as pd
import os
import mlflow
import mlflow.sklearn
from src.utils.common import read_yaml, save_object
from sklearn.linear_model import ElasticNet
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
import joblib
from pathlib import Path

class ModelTrainer:
    def __init__(self, config_path):
        self.config = read_yaml(Path(config_path))

    def eval_metrics(self, actual, pred):
        rmse = np.sqrt(mean_squared_error(actual, pred))
        mae = mean_absolute_error(actual, pred)
        r2 = r2_score(actual, pred)
        return rmse, mae, r2

    def initiate_model_trainer(self, X_train, X_test, y_train, y_test):
        try:
            print("🚀 Model training and Optimization is starting...")
            
            # 1. Models and Hyperparameters
            models = {
                "ElasticNet": {
                    "model": ElasticNet(),
                    "params": {
                        "alpha": [0.1, 0.5, 1.0],
                        "l1_ratio": [0.1, 0.5, 0.9]
                    }
                },
                "RandomForest": {
                    "model": RandomForestRegressor(),
                    "params": {
                        "n_estimators": [50, 100],
                        "max_depth": [5, 10, None]
                    }
                },
                "XGBoost": {
                    "model": XGBRegressor(),
                    "params": {
                        "n_estimators": [50, 100],
                        "learning_rate": [0.01, 0.1],
                        "max_depth": [3, 5]
                    }
                }
            }

            best_model_name = ""
            best_model_score = -1 # R2 score for (best)
            best_model_obj = None
            best_params = None

            mlflow.set_experiment(self.config['mlflow']['experiment_name'])

            # 2. Loop: Try each model
            for model_name, model_info in models.items():
                print(f"🥊 {model_name} training...")   
                
                with mlflow.start_run(run_name=f"Tuning_{model_name}", nested=True):
                    # GridSearchCV ile Cross-Validation (5-Fold)
                    grid_search = GridSearchCV(
                        estimator=model_info['model'],
                        param_grid=model_info['params'],
                        cv=5,            # 5 Fold Cross Validation
                        n_jobs=-1,       # Use all processors
                        scoring='r2',    # Success criterion R2 Score
                        verbose=1
                    )
                    
                    grid_search.fit(X_train, y_train)
                    
                    # Get the best version of the model
                    current_best_model = grid_search.best_estimator_
                    current_best_params = grid_search.best_params_
                    
                    # Test data prediction
                    predicted = current_best_model.predict(X_test)
                    (rmse, mae, r2) = self.eval_metrics(y_test, predicted)
                    
                    print(f"   ✅ {model_name} -> R2: {r2:.4f}, RMSE: {rmse:.4f}")
                    
                    # Log to MLflow (Save each attempt)
                    mlflow.log_params(current_best_params)
                    mlflow.log_metric("rmse", rmse)
                    mlflow.log_metric("r2", r2)
                    mlflow.sklearn.log_model(current_best_model, model_name)

                    # Update Champion
                    if r2 > best_model_score:
                        best_model_score = r2
                        best_model_name = model_name
                        best_model_obj = current_best_model
                        best_params = current_best_params

            print(f"🏆 Champion Model: {best_model_name} (R2: {best_model_score:.4f})")
            
            # 3. Save the best model   
            with mlflow.start_run(run_name="Best_Model_Production"):
                mlflow.log_param("best_model", best_model_name)
                mlflow.log_params(best_params)
                mlflow.log_metric("rmse", rmse) # Champion's score
                mlflow.log_metric("r2", best_model_score)
                
                mlflow.sklearn.log_model(
                    best_model_obj, 
                    "model",
                    registered_model_name=self.config['mlflow']['model_name']
                )

                save_object(
                    file_path=os.path.join("models", "model.joblib"),
                    obj=best_model_obj
                )
                
                print(f"✅ Model saved as: models/model.joblib")

        except Exception as e:
            print(f"❌ Model training error: {e}")
            raise e