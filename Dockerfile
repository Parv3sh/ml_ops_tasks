FROM python:3.8-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the Python scripts
COPY tune_model.py tune_model.py
COPY aggregate_results.py aggregate_results.py

CMD ["python", "tune_model.py"]
