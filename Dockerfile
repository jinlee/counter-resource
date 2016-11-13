FROM python:2.7

RUN apt-get update && apt-get install -y python-pip
RUN pip install boto3

COPY check.py /opt/resource/check
COPY in.py    /opt/resource/in
COPY out.py   /opt/resource/out
