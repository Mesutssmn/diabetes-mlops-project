# 🩺 End-to-End Diabetes Prediction MLOps System

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B)
![MLflow](https://img.shields.io/badge/MLflow-Tracking-0194E2)
![License](https://img.shields.io/badge/License-MIT-green)

## 📖 Project Overview
This project implements a complete **Full-Stack MLOps pipeline** for predicting diabetes disease progression based on physiological and blood serum measurements. It is designed to be **robust, scalable, and fully containerized**.

The system automates the entire lifecycle:
1.  **Data Ingestion & Validation**
2.  **Model Training** (ElasticNet Regression)
3.  **Experiment Tracking** (MLflow)
4.  **Model Deployment** (FastAPI)
5.  **User Interface** (Streamlit Web App)

---

## 🏗️ Architecture

The project runs on a multi-container Docker architecture:

* **`diabetes_frontend`**: Interactive web interface built with **Streamlit** for end-users.
* **`diabetes_api`**: The backend service (**FastAPI**) that serves the model. It includes a "Lazy Loading" mechanism to fetch the model from MLflow dynamically.
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

3.  **Train the Model (First Run Only):**
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

## 💻 Usage

### 1. Web Interface (Streamlit)
The easiest way to use the model.
* **URL:** [http://localhost:8501](http://localhost:8501)
* Enter the patient's physiological and blood serum data.
* Click **"Predict Progression"** to see the result and risk analysis.

### 2. API Documentation (Swagger UI)
For developers who want to integrate the model.
* **URL:** [http://localhost:8000/docs](http://localhost:8000/docs)
* **Endpoint:** `POST /predict`

#### Example Request Body
```json
{
  "age": 59,
  "sex": 2,
  "bmi": 32.1,
  "bp": 101,
  "s1": 157,
  "s2": 93.2,
  "s3": 38,
  "s4": 4,
  "s5": 4.85,
  "s6": 87
}