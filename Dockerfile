FROM python:3.7
MAINTAINER Vladimir Pushkarev
RUN mkdir /app

ENV HOME=/app
ENV PYTHONPATH=$HOME
ENV PYTHONDONTWRITEBYTECODE yes

WORKDIR $HOME

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt && rm requirements.txt

COPY static static
COPY index.html .
COPY sioserver.py .
