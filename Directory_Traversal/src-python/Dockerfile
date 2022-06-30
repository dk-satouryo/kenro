FROM python:3.9.2-alpine

WORKDIR /app
COPY ./app/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY ./app /app
CMD ["python", "app.py"]