FROM python:3.11-slim

RUN pip install mlflow==2.11.3 sqlalchemy boto3 pymysql

WORKDIR /mlflow

EXPOSE 5000

CMD ["echo", "MLflow container ready"]