# Pull base image
FROM python:3.7-slim
#FROM ubuntu
# Set environment varibles
ENV PYTHONUNBUFFERED 1

# Set work directory
RUN mkdir /code
RUN apt-get update && apt-get install -y gromacs
#RUN apt install -y python2.7
RUN pip install --upgrade pip && \
    pip install --no-cache-dir matplotlib
WORKDIR /code
RUN apt install -y python2.7

# Install dependencies
COPY requirements.txt /code/
RUN pip install -r requirements.txt


# Copy project
COPY . /code/
