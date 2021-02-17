FROM python:3.9-slim-buster

RUN mkdir /cenozoa
WORKDIR /cenozoa

ADD requirements.txt /cenozoa
RUN pip install -r /cenozoa/requirements.txt
RUN pip install gunicorn

ADD cenozoa /cenozoa
RUN chmod +x /cenozoa/run.sh

ENV FLASK_APP=/cenozoa/server.py
ENV FLASK_ENV=development

CMD ["/bin/bash", "./run.sh"]

