# 10/1/2018
FROM python:3-onbuild

RUN mkdir /code

WORKDIR /code

ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/


