FROM python:3.9-slim

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN rm requirements.txt

COPY src/ app/
WORKDIR app/
