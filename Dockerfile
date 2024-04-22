FROM python:3.9.5
LABEL authors="CalMaru <cal@42maru.ai>"

ENV HOME /es-ojt
RUN mkdir -p ${HOME}
WORKDIR ${HOME}

RUN apt-get update && apt-get -y install vim

########## set virtual environment ##########
RUN pip install poetry==1.7.1
RUN poetry config virtualenvs.create false

########## install dependencies ##########
COPY pyproject.toml ${HOME}
RUN poetry lock --no-update && poetry install --no-dev

########## copy code ##########
COPY ./app ${HOME}
