FROM python:3
WORKDIR /app
COPY . /app
RUN pip install -r requeriments.txt
CMD python ./app.py