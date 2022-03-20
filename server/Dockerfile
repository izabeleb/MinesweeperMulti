FROM python:3.10-alpine3.15

COPY / /app

RUN pip install --requirement /app/requirements.txt \
    && rm /app/requirements.txt

EXPOSE 5000

ENTRYPOINT python /app/app.py