FROM python:3.9-slim-buster

WORKDIR /mlh-fellowship-project

COPY requirements_home.txt .

RUN pip3 install -r requirements_home.txt

COPY . .

CMD ["flask", "run", "--host=0.0.0.0"]

EXPOSE 5000
