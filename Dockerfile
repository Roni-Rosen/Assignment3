# FROM python:3.11-slim-bullseye

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ENV FLASK_APP=main.py
ENV FLASK_RUN_PORT=8000

CMD ["flask", "run", "--host", "0.0.0.0"]