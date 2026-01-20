import pandas as pd
import uvicorn
from fastapi import FastAPI, HTTPException
from src.api.schemas.prediction import DiabetesInput
from src.utils.common import read_yaml, load_object
import os
from pathlib import Path
import mlflow
from mlflow.tracking import MlflowClient

app = FastAPI(
    title="Diabetes Prediction API",
    description="MLOps Pipeline - Diabetes Disease Progression Prediction",
    version="1.0.0"
)

# --- CONFIG & GLOBALS ---
config_path = Path("configs/config.yaml")
config = read_yaml(config_path)

# MLflow Settings
MLFLOW_TRACKING_URI = config['mlflow']['tracking_uri']
model_name = config['mlflow']['model_name'] 
stage = "Production"

# Model & Scaler Global Variables
model = None
scaler = None

def load_artifacts():
    """
    Model & Scaler load from MLflow or local file.
    """
    global model, scaler
    
    # 1. MODEL YÜKLEME
    try:
        # Önce MLflow'dan çekmeyi dene (Localhost/Geliştirme Ortamı)
        print(f"🔄 Connecting to MLflow at {MLFLOW_TRACKING_URI}...")
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        client = MlflowClient()
        
        model_production_uri = f"models:/{model_name}/{stage}"
        model = mlflow.sklearn.load_model(model_production_uri)
        print("✅ Model loaded from MLflow Registry")
        
    except Exception as e:
        print(f"⚠️ MLflow connection failed: {e}")
        print("🔄 Switching to local file loading (Offline/Render Mode)...")
        
        try:
            # Başarısız olursa yerel dosyadan yükle (Render/Production)
            local_model_path = os.path.join("models", "model.joblib")
            model = load_object(local_model_path)
            print(f"✅ Model loaded from local file ({local_model_path})")
        except Exception as e2:
            print(f"❌ FATAL: Could not load model from file either: {e2}")
            model = None

    # 2. SCALER LOADING
    try:
        # Scaler genelde dosya olarak durur
        local_scaler_path = os.path.join("models", "scaler.joblib")
        scaler = load_object(local_scaler_path)
        print(f"✅ Scaler loaded from {local_scaler_path}")
    except Exception as e:
        print(f"❌ Scaler loading failed: {e}")
        scaler = None

@app.on_event("startup")
def startup_event():
    print("🚀 API is starting up...")
    load_artifacts()

@app.get("/")
def read_root():
    return {"message": "Diabetes Prediction API is Live! Go to /docs for Swagger UI."}

@app.post("/predict", 
          summary="Predict Diabetes Progression",
          description="Predicts disease progression based on physiological metrics.")
def predict(data: DiabetesInput):
    # Global variables
    
    # Model & Scaler not found, attempting to reload...
    if model is None or scaler is None:
        # Lazy Loading: Tekrar yüklemeyi dene
        print("⚠️ Model/Scaler not found, attempting to reload...")
        load_artifacts()
        if model is None or scaler is None:
             raise HTTPException(status_code=503, detail="Model or Scaler not available. Service is initializing or failed.")

    try:
        # 1. DataFrame
        input_df = pd.DataFrame([data.dict()])
        
        # 2. Scaling
        scaled_data = scaler.transform(input_df)
        
        # 3. Prediction
        prediction = model.predict(scaled_data)
        
        return {"prediction": float(prediction[0])}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction Error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)