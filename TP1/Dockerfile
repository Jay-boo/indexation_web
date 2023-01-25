FROM python:3.8

RUN mkdir /crawler
WORKDIR /crawler

COPY  requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY crawl/ crawl/
COPY main.py main.py


ENTRYPOINT [ "python" ,"main.py","--url","https://ensai.fr","--limit_pages","60","--multithread","False"]
