FROM python:3
ENV PYTHONBUFFERED 1
RUN mkdir /saphire-backend
WORKDIR /saphire-backend 
COPY requirements.txt /saphire-backend/
RUN pip install -r requirements.txt
COPY . /saphire-backend/