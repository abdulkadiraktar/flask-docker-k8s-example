
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt /app
#Paketleri yukle
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py /app
EXPOSE 5000
CMD ["python", "app.py"]