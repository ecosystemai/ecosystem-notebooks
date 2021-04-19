# docker build -t ecosystem-dashboards:latest .
# docker run -d -p 5000:5000 ecosystem-dashboards

FROM ubuntu:18.04

MAINTAINER Ramsay Louw "Ramsay@ecosystem.ai"

RUN apt-get update
RUN apt-get purge python
RUN apt-get install python3.6 -y
RUN apt-get install python3-pip -y

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . /app

CMD ["gunicorn", "-w 1", "-b 0.0.0.0:5000", "esd_boot:server", "--timeout 600", "--keep-alive 600"]