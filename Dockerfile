FROM python:3.11-slim

LABEL authors="sergiusz"

WORKDIR /backend

COPY /backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
