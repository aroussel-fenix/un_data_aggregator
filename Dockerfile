FROM python:3

WORKDIR /src/

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY ./acquire_data ./acquire_data

WORKDIR /src/acquire_data/

CMD [ "python", "-c", "import fetcher; fetcher.run()" ]
