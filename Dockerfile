FROM python:3.12-slim
LABEL authors="gloomforge"

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 4200

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "4200"]