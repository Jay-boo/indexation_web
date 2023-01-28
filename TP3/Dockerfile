FROM python:3.8

RUN mkdir /TPquery
WORKDIR /TPquery

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY  query/ query/
COPY test/ test/
COPY main.py main.py
COPY index.json index.json
COPY documents.json documents.json

#-------------
# Assert test passed before launching
RUN python3 -m unittest discover test

ENTRYPOINT [ "python3" ,"main.py","--Q","karine wikipédia"]
# ENTRYPOINT [ "python3","-m", "unittest","discover","test" ]


