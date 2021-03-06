FROM python:3.9.6

WORKDIR /app

COPY requirements.txt /app/
RUN pip3 install -r requirements.txt

RUN groupadd -r default && useradd -r -g default default
USER default

COPY . /app/

EXPOSE 8000

WORKDIR /app/medium_clone

ENTRYPOINT ["gunicorn", "-c", "../conf/gunicorn.config.py"]
