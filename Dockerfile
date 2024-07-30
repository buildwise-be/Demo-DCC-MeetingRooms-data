FROM ubuntu:22.04
RUN mkdir /webdrivers /src

COPY ./webdrivers/* /webdrivers

RUN apt-get update && \
    apt-get install -y --no-install-recommends ./webdrivers/google-chrome-stable_current_amd64.deb python3-pip build-essential libpq-dev python3-dev

COPY requirements.txt /

RUN pip install -r /requirements.txt

COPY ./src /src
WORKDIR /src

CMD ["python3", "run.py"]