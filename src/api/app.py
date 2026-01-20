from fastapi import FastAPI, HTTPException
import mlflow.sklearn
import pandas as pd
import joblib
import os
import socket
from src.api.schemas.prediction import DiabetesInput
from src.utils.common import read_yaml
from pathlib import Path

app = FastAPI(title="Diabetes Prediction Service")

model = None
scaler = None

def resolve_mlflow_uri(uri_or_host):
    try:
        if "://" in uri_or_host:
            protocol, address = uri_or_host.split("://")
            host = address.split(":")[0]
            port = address.split(":")[1] if ":" in address else "5000"
        else:
            host = uri_or_host
            port = "5000"
            protocol = "http"
        ip_address = socket.gethostbyname(host)
        return f"{protocol}://{ip_address}:{port}"
    except:
        return uri_or_host

def load_artifacts():
    global model, scaler
    print("🔄 Model and Scaler loading...")
    try:
        config = read_yaml(Path("configs/config.yaml"))
        
        if scaler is None:
            scaler_path = os.path.join(config['artifacts']['model_dir'], "scaler.joblib")
            if os.path.exists(scaler_path):
                scaler = joblib.load(scaler_path)
                print(f"✅ Scaler loaded.")
            else:
                print("⚠️ Scaler file not found.")

        if model is None:
            mlflow_host = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow_server:5000")
            resolved_uri = resolve_mlflow_uri(mlflow_host)
            mlflow.set_tracking_uri(resolved_uri)
            
            model_name = config['mlflow']['model_name']
            model_uri = f"models:/{model_name}/Production"
            
            print(f"📡 Connecting to MLflow: {resolved_uri}")
            model = mlflow.sklearn.load_model(model_uri)
            print("✅ Model loaded successfully from MLflow!")
            
        return True
    except Exception as e:
        print(f"❌ Loading Error: {e}")
        return False

@app.on_event("startup")
def startup_event():
    load_artifacts()

@app.post("/predict", 
          summary="Predict Diabetes Progression",
          description="""
          This endpoint predicts the disease progression measure based on patient metrics.
          
          **Input Descriptions:**
          * **age:** Patient's age in years.
          * **sex:** Patient's sex (2 for female, 1 for male).
          * **bmi:** Body Mass Index.
          * **bp:** Blood Pressure.
          * **s1 (tc):** Total Serum Cholesterol
          * **s2 (ldl):** Low-Density Lipoproteins
          * **s3 (hdl):** High-Density Lipoproteins
          * **s4 (tch):** Total Cholesterol / HDL Ratio
          * **s5 (ltg):** Log of Serum Triglycerides Level
          * **s6 (glu):** Blood Sugar Level
          """)
def predict(data: DiabetesInput):
    global model, scaler
    
    if model is None or scaler is None:
        print("⚠️ Model not loaded, loading now...")
        success = load_artifacts()
        if not success:
            raise HTTPException(status_code=503, detail="Model not loaded. Please make sure MLflow is running and the model is in Production.")

    try:
        input_data = data.dict()
        df = pd.DataFrame([input_data])
        
        if scaler:
            df_scaled = scaler.transform(df)
        else:
            df_scaled = df
            
        prediction = model.predict(df_scaled)
        result = float(prediction[0])
        print(f"🎯 Prediction: {result}")
        
        return {"prediction": result}
        
    except Exception as e:
        print(f"⚠️ Prediction Error: {e}")
        return {"error": str(e)}