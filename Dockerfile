# start by pulling the python image
FROM python:3.9-alpine

COPY requirements.txt /
RUN pip3 install -r /requirements.txt
COPY . /app
WORKDIR /app
EXPOSE 5200
CMD ["gunicorn", "--bind", "0.0.0.0:5200", "wsgi:app"]
