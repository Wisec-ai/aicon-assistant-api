FROM python:3.10.16-slim

WORKDIR /api
COPY . /api

RUN apt update -y \
    && apt-get upgrade -y \
    && apt-get install -y git \
    && apt install -y build-essential gcc libpq-dev ffmpeg libsm6 libxext6 libzbar0 python3-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install -r requirements.txt 

EXPOSE 8080

CMD ["python", "manage.py", "runserver","0.0.0.0:8080"]