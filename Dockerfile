FROM python:3.9-slim-buster

WORKDIR /root/GitHub/mlh-fellowship-project/

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

CMD ["flask", "run", "--host=0.0.0.0", "-p 80"]

EXPOSE 80
