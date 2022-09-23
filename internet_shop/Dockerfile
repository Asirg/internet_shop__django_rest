FROM python:3.10
# Заргружаем образ для python

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Установка виртуальных переменных

WORKDIR /usr/src/web
# Установка директории внутри контейнера, которая будет рабочей

COPY ./req.txt /usr/src/req.txt
RUN pip install --upgrade pip
RUN python3 -m pip install -r /usr/src/req.txt


COPY . /usr/src/web