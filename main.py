from flask import Flask, Response, request
from metrics_service import MetricService
from models import Metric

import json

app= Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/<name>")
def hello_name(name):
    return "Hello "+ name

@app.route("/metric", methods=["POST"])
def metric():
    resp = MetricService().create(request.get_json())
    return Response(status=201)

if __name__ == "__main__":
    app.run(debug=True)

