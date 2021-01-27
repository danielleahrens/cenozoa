from flask import Flask, Response, request
from metrics_service import MetricService
from models import Metric
from config import config

import json

metric_service = MetricService()

app= Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/<name>")
def hello_name(name):
    return "Hello "+ name

@app.route("/metric", methods=["POST"])
def metric():
    resp = metric_service.create(request.get_json())
    return Response(status=201)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

