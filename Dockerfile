FROM python:3.8-slim

WORKDIR /src/

COPY . .

RUN pip install pipenv \
        && pipenv install \
        && pipenv shell

CMD [ "python", "-c", "from acquire_data.fetcher import Fetcher; Fetcher().run()" ]
