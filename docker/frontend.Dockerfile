FROM python:3.11-slim

WORKDIR /app

# Gerekli kütüphaneleri kur
RUN pip install streamlit requests

# Kod dosyasını kopyala
COPY frontend/app.py /app/app.py

# Streamlit'in kullandığı portu dışarı aç
EXPOSE 8501

# Çalıştırma komutu
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]