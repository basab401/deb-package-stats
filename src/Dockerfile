FROM ubuntu:bionic
MAINTAINER Basabjit "basab401@yahoo.co.in"

ENV DEBIAN_FRONTEND noninteractive

ENV https_proxy $HTTP_PROXY
ENV http_proxy $HTTP_PROXY

RUN apt-get update \
  && apt-get -y install python3-pip \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

WORKDIR /package_statistics
COPY ./package_stats_lib ./package_stats_lib
COPY ./package_statistics.py ./package_statistics.py
COPY ./tests ./tests
COPY ./setup.py .
COPY ./requirements.txt .

# Install the package
RUN pip3 install -r requirements.txt \
    && python3 setup.py install
    # To install wheel instead of egg
    # python3 setup.py sdist bdist_wheel \
    # && pip3 install dist/package_statistics-1.0.1-py3-none-any.whl

RUN apt-get clean -y; apt-get autoclean -y; apt-get autoremove -y

ENTRYPOINT ["/bin/bash"]