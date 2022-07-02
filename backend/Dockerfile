FROM python:3.8.5
WORKDIR /app
RUN pip install --upgrade pip && pip install -r /app/requirements.txt
COPY . .
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]