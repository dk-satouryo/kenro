FROM python:3.9.2-alpine3.12

WORKDIR /app
RUN apk --update-cache add gcc libc-dev g++
COPY ./app/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY ./app /app
CMD ["python", "app.py"]
