FROM python:3.12.10 AS base
WORKDIR /app
ADD requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app/main.py"]
EXPOSE 8080