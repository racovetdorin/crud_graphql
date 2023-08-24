FROM python:3.11 as python-base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

WORKDIR  /app

COPY /pyproject.toml /app/

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install 

COPY . .

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
