FROM python:3.10-slim
WORKDIR /app
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir --default-timeout=1000 --retries 5 -r requirements.txt
COPY app.py .
CMD ["python", "app.py"]