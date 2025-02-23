FROM python:3.9-slim

RUN apt-get update && apt-get install -y postgresql-client

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "Main:app", "--host", "0.0.0.0", "--port", "8000"]