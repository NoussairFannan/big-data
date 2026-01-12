FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy consumer code
COPY kafka_to_hdfs.py .

# Run consumer
CMD ["python", "kafka_to_hdfs.py"]