FROM python:3.10-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH=.
ENV PYTHONUNBUFFERED 1
#ENV ENVIRONMENT prod
ENV TESTING 0


COPY ./requirements.txt .

#RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
RUN apt-get update  \
    && pip install -r ./requirements.txt \
    && rm -rf /root/.cache/pip \
    && apt-get clean autoclean \
    && apt-get autoremove --yes \
    && rm -rf /var/lib/{apt,dpkg,cache,log}/


COPY . .

