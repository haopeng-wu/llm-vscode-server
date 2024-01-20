FROM python:3.8
WORKDIR /src
ADD requirements.txt requirements.txt
ADD . /src
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD gunicorn --workers=2 main:app -b 127.0.0.1:5000