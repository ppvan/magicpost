FROM python:3.10.12
WORKDIR /code

COPY ./Pipfile ./Pipfile.lock /code/
RUN pip install pipenv && pipenv install --deploy --system --ignore-pipfile

COPY ./magicpost /code/magicpost


CMD ["uvicorn", "magicpost.app:app", "--host", "0.0.0.0", "--port", "80"]