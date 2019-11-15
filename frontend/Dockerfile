FROM python:3.7
ENV PYTHONUNBUFFERED=TRUE
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
