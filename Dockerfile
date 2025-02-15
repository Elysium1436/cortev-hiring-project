FROM python:3.13

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # Poetry's configuration:
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local' \
  POETRY_VERSION=2.0.1


RUN echo ${POETRY_HOME} $POETRY_HOME
RUN cd /usr/local && ls

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /APP
COPY poetry.lock pyproject.toml /APP/

RUN poetry install --no-interaction --no-ansi

COPY . /APP



CMD [ "poetry", "run", "gunicorn", "corteva_weather.wsgi:application", "--bind", "0.0.0.0:8000" ]