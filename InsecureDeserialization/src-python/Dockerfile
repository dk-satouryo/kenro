FROM python:3.9.2-alpine

WORKDIR /app
COPY ./app/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

RUN addgroup -S user01
RUN adduser -S user01 -G user01
COPY --chown=user01:user01 ./app /app
RUN chmod 555 /app

RUN addgroup -S user02
RUN adduser -S user02 -G user02
USER user02
CMD ["python", "app.py"]