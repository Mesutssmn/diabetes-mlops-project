import os
import pandas as pd
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from src.utils.common import read_yaml, create_directories
from pathlib import Path

class DataIngestion:
    def __init__(self, config_path: Path):
        self.config = read_yaml(config_path)
        
    def initiate_data_ingestion(self):
        try:
            # 1. Load data (Scikit-learn diabetes dataset)
            diabetes = load_diabetes(scaled = False)
            df = pd.DataFrame(diabetes.data, columns=diabetes.feature_names)
            df['target'] = diabetes.target
            
            # 2. Create directories
            raw_data_path = Path(self.config['data']['raw_path'])
            create_directories([raw_data_path.parent])
            
            # 3. Save raw data
            df.to_csv(raw_data_path, index=False)
            print(f"Data saved successfully: {raw_data_path}")
            
            return raw_data_path
            
        except Exception as e:
            raise e

if __name__ == "__main__":
    # Test running
    ingestion = DataIngestion(Path("configs/config.yaml"))
    ingestion.initiate_data_ingestion()