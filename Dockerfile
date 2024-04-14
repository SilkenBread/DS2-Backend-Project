FROM python:3.9-alpine3.14
ENV PYTHONUNBUFFERED=1

WORKDIR /drf_ds2
ADD requirements.txt /drf_ds2/

RUN pip install --upgrade pip && \
    pip install -r requirements.txt
