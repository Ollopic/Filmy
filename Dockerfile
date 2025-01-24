FROM python:3.13

RUN apt-get update && apt-get install -y curl

RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - &&\
apt-get install -y nodejs

WORKDIR /app

COPY ./requirements.txt /app

RUN pip install -r requirements.txt

RUN npm install

CMD ["flask", "run", "--debug", "--host=0.0.0.0"]