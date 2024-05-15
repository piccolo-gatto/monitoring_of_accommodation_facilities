FROM python:3.12

WORKDIR /app

RUN pip install poetry

COPY poetry.lock pyproject.toml ./

RUN poetry install

COPY . .

EXPOSE 8050

CMD ["poetry", "run", "python", "main.py"]
