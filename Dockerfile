FROM python:3.8
WORKDIR /app
ADD requirements.txt requirements.txt
ADD conf.yml conf.yml
ADD main.py main.py
ADD .env-35-16k.yml .env-35-16k.yml
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD python main.py