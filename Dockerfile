FROM python:3.9-buster

RUN apt-get update && apt-get install -y make cmake

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD [ "make", "run-api-locally" ]