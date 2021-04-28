FROM python:3.8-slim

WORKDIR /src/

COPY . .

RUN apt-get update \ 
        && apt-get --no-install-recommends --no-install-suggests --yes --quiet install pipenv \
        && pipenv install

CMD [ "pipenv" "run" "python", "-c", "from acquire_data.fetcher import Fetcher; Fetcher().run()" ]
