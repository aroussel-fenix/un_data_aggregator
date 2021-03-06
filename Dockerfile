FROM python:3.6.10-slim-buster

WORKDIR /src/

COPY . .

RUN pipenv install

CMD [ "python", "-c", "from acquire_data.fetcher import Fetcher; Fetcher().run()" ]
