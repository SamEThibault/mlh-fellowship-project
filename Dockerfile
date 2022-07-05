FROM python:3.9-slim-buster

WORKDIR /mlh-fellowship-project

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .
RUN pip install peewee PyMySQL
CMD ["flask", "run", "--host=0.0.0.0", "-p 80"]

EXPOSE 80
