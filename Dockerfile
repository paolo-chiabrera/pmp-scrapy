FROM python:3.6-jessie

RUN apt-get update && apt-get upgrade -y

RUN pip install --upgrade pip

RUN pip install scrapy

ADD requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt && rm /tmp/requirements.txt

# Expose web GUI
EXPOSE 6800

COPY . /opt/app

RUN cd /opt/app

CMD [ "scrapy crawl piccsy -L INFO" ]