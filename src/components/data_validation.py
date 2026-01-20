import pandas as pd
from pathlib import Path
from src.utils.common import read_yaml

class DataValidation:
    def __init__(self, config_path: Path, schema_path: Path):
        self.config = read_yaml(config_path)
        self.schema = read_yaml(schema_path)

    def validate_all_columns(self) -> bool:
        try:
            validation_status = None
            data = pd.read_csv(self.config['data']['raw_path'])
            all_cols = list(data.columns)
            expected_schema = self.schema['COLUMNS']

            for col in all_cols:
                if col not in expected_schema:
                    validation_status = False
                    print(f"Error: {col} column not found in expected schema!")
                elif data[col].dtype != expected_schema[col]:
                    validation_status = False
                    print(f"Error: {col} column type is wrong! Expected: {expected_schema[col]}")
                else:
                    validation_status = True
            
            # Write status to a file (for pipeline tracking)
            with open("status.txt", "w") as f:
                f.write(f"Validation status: {validation_status}")

            return validation_status

        except Exception as e:
            raise e