from python:3.14-slim
workdir /app
copy requirements.txt .
run pip install --no-cache-dir -r requirements.txt
copy app.py frontend.py random_forest_model.joblib ./
copy templates ./templates
copy static ./static
expose 8000
cmd ["sh", "-c", "exec python -m uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}"]
