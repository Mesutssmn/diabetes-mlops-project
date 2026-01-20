# 🩺 End-to-End Diabetes Prediction MLOps Pipeline

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688)
![MLflow](https://img.shields.io/badge/MLflow-Tracking-0194E2)
![License](https://img.shields.io/badge/License-MIT-green)

## 📖 Project Overview
This project implements a complete **MLOps pipeline** for predicting diabetes disease progression based on physiological and blood serum measurements. It is designed to be **robust, scalable, and containerized**.

The system automates the entire lifecycle:
1.  **Data Ingestion & Validation**
2.  **Model Training** (ElasticNet Regression)
3.  **Experiment Tracking** (MLflow)
4.  **Model Deployment** (FastAPI)
5.  **Serving** (REST API with Docker)

---

## 🏗️ Architecture

The project runs on a multi-container Docker architecture:

* **`diabetes_api`**: The backend service (FastAPI) that serves the model. It includes a "Lazy Loading" mechanism to fetch the model from MLflow dynamically.
* **`mlflow_server`**: A centralized tracking server for model registry, experiments, and artifact storage (SQLite backend).

---

## 🚀 Quick Start

### Prerequisites
* Docker & Docker Compose

### Installation & Running
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/diabetes-mlops-project.git](https://github.com/YOUR_USERNAME/diabetes-mlops-project.git)
    cd diabetes-mlops-project
    ```

2.  **Build and Start Services:**
    ```bash
    docker-compose up -d --build
    ```

3.  **Train the Model:**
    The API needs a trained model. Trigger the pipeline inside the container:
    ```bash
    docker exec -it diabetes_api python main.py
    ```

4.  **Register the Model:**
    * Go to MLflow UI: [http://localhost:5000](http://localhost:5000)
    * Find `DiabetesElasticNetModel`.
    * Transition the latest version to **"Production"**.

5.  **Restart API (to load the new model):**
    ```bash
    docker-compose restart api
    ```

---

## ⚡ API Usage

The API provides interactive documentation via Swagger UI.

* **URL:** [http://localhost:8000/docs](http://localhost:8000/docs)
* **Endpoint:** `POST /predict`

### Example Request Body
```json
{
  "age": 0.038,
  "sex": 0.05,
  "bmi": 0.061,
  "bp": 0.021,
  "s1": -0.044,
  "s2": -0.034,
  "s3": -0.043,
  "s4": -0.002,
  "s5": 0.019,
  "s6": -0.017
}