FROM python:3.7

ADD getMyMovies.py /code/
ADD requirements.txt /code/

WORKDIR /code

RUN pip install -r requirements.txt

