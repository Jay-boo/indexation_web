FROM python:3.8

RUN mkdir /index
WORKDIR /index

COPY  requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY indexWeb/ indexWeb/
COPY main.py main.py
COPY crawled_urls.json crawled_urls.json



ENTRYPOINT [ "python" ,"main.py"]
