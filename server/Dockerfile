FROM python:3.10-alpine3.15 as builder

RUN mkdir /app
COPY /app.py /requirements.txt /app/
COPY /minesweeper /app/minesweeper

RUN pip install --requirement /app/requirements.txt \
    && rm /app/requirements.txt

EXPOSE 5000

ENTRYPOINT python /app/app.py