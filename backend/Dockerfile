FROM python:3.8.5
WORKDIR /app
COPY . .
RUN pip install --upgrade pip && pip install -r /app/requirements.txt
CMD gunicorn foodgram_api.wsgi:application --bind 0.0.0.0:8000