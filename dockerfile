FROM python:3.9-slim 

WORKDIR /api_project

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]

EXPOSE 9090