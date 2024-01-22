FROM python:3.8
WORKDIR /app
ADD requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD python main.py