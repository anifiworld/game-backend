FROM python:3.10.4-slim-buster AS poetry
RUN pip install poetry
WORKDIR /code
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry export -f requirements.txt --without-hashes --output requirements.txt

FROM python:3.10.4-slim-buster
WORKDIR /code
COPY --from=poetry /code/requirements.txt .
COPY entrypoint.sh .

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get -y install gcc && \
    rm -rf /var/lib/apt/lists/*

RUN pip install pip --upgrade && \
    pip install -r requirements.txt && \
    chmod +x entrypoint.sh
COPY . .

STOPSIGNAL SIGINT

CMD ["sh", "entrypoint.sh"]