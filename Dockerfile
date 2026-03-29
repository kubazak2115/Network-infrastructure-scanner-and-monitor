FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN g++ -o scanner/scanner scanner/scanner.cpp -pthread

EXPOSE 5000

CMD ["python", "main.py"]