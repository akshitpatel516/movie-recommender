FROM python:3.10-slim

WORKDIR /app

# Upgrade pip first (important)
RUN pip install --upgrade pip

# Copy only requirements first (layer caching)
COPY requirements.txt .

# Increase timeout + disable progress bar (more stable)
RUN pip install \
    --no-cache-dir \
    --default-timeout=1000 \
    --progress-bar off \
    -r requirements.txt

# Copy rest of the code
COPY . .

EXPOSE 8000
EXPOSE 8501

CMD uvicorn app.main:app --host 0.0.0.0 --port 8000 & \
    streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0
