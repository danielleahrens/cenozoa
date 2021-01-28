from flask import Flask, Response, request
from metrics_service import MetricService
from models import Metric
from config import config
from nosqldb_service import nosqldb_service

import json

metric_service = MetricService()

app= Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/<name>")
def hello_name(name):
    return "Hello "+ name

@app.route("/sensor/metric", methods=["POST"])
def metric():
    request_obj = request.get_json()
    print(f'heres the request object {request_obj}')
    #TODO: probably don't need to query database for every metric request,
    # probs load all sensor IDs into memory and consulting that.
    sensors = nosqldb_service.get_sensor(request_obj['sensor_id'])
    print(f'get sensors: {sensors}')
    if (len(sensors) == 0):
        print(f'no sensors with ID found, creating new sensor')
        nosqldb_service.new_sensor(request_obj['sensor_type'], request_obj['sensor_id'])
    resp = metric_service.create(request_obj)
    return Response(status=201)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

