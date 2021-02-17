FROM python:3.9-slim-buster

RUN mkdir /cenozoa
WORKDIR /cenozoa

ADD requirements.txt /cenozoa
RUN pip install -r /cenozoa/requirements.txt
RUN pip install gunicorn

ADD cenozoa /cenozoa

ENV FLASK_APP=/cenozoa/server.py
ENV FLASK_ENV=development

# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app", "--log-level", "debug"]
CMD ["/run.sh"]

