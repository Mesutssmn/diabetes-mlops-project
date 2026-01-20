import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
from pathlib import Path
from src.utils.common import read_yaml

class DataTransformation:
    def __init__(self, config_path: Path):
        self.config = read_yaml(config_path)

    def get_transformer_object(self):
        # Create scaler to normalize data
        return StandardScaler()

    def initiate_data_transformation(self):
        try:
            # 1. Load data
            data = pd.read_csv(self.config['data']['raw_path'])

            # 2. Train-Test Split
            train, test = train_test_split(
                data, test_size=self.config['data']['test_size'], random_state=42
            )

            # 3. Separate independent and dependent variables
            target_col = 'target'
            X_train = train.drop([target_col], axis=1)
            y_train = train[target_col]
            X_test = test.drop([target_col], axis=1)
            y_test = test[target_col]

            # 4. Scaling
            scaler = self.get_transformer_object()
            
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)

            # 5. Save scaler (very important for API)
            scaler_path = os.path.join(self.config['artifacts']['model_dir'], "scaler.joblib")
            joblib.dump(scaler, scaler_path)

            # 6. Save transformed data (optional but good for tracking)
            train_path = os.path.join("data/processed", "train.csv")
            test_path = os.path.join("data/processed", "test.csv")
            
            pd.DataFrame(X_train_scaled, columns=X_train.columns).to_csv(train_path, index=False)
            pd.DataFrame(X_test_scaled, columns=X_test.columns).to_csv(test_path, index=False)

            print(f"✅ Data transformation completed. Scaler saved: {scaler_path}")
            return X_train_scaled, X_test_scaled, y_train, y_test

        except Exception as e:
            raise e