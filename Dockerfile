FROM python:3.12

WORKDIR /code

RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.7.1 \
    && $HOME/.local/bin/poetry config cache-dir /root/.cache/pypoetry \
    && $HOME/.local/bin/poetry config virtualenvs.in-project true

COPY ./poetry.lock ./pyproject.toml /code/

RUN $HOME/.local/bin/poetry install --only main --no-root --no-interaction --no-ansi --verbose \
 && rm -r /root/.cache/pypoetry

COPY ./main.py /code/main.py

CMD [".venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
