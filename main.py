from flask import Flask, Response, request, jsonify
from metrics_service import MetricService
from models import Metric
from config import config
from nosqldb_service import new_sensor, get_sensor, update_location

import json

metric_service = MetricService()

app= Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/<name>")
def hello_name(name):
    return "Hello "+ name

@app.route("/sensor", methods=["GET", "PUT"])
def sensor():
    if request.method == 'GET':
        locations = request.args.getlist('l')
        resp = get_sensor(locations=locations)
        return jsonify(resp), 201

    if request.method == 'PUT':
        request_obj = request.get_json()
        verify_sensor(request_obj['sensor_type'], request_obj['sensor_id'])
        update_location(request_obj['sensor_id'], request_obj['location'])
    return Response(status=201)

@app.route("/sensor/metric", methods=["POST"])
def metric():
    request_obj = request.get_json()
    #TODO: probably don't need to query database for every metric request,
    # probs load all sensor IDs into memory and consulting that.
    verify_sensor(request_obj['sensor_type'], request_obj['sensor_id'])
    resp = metric_service.create(request_obj)
    return Response(status=201)

def verify_sensor(sensor_type, sensor_id):
    sensors = get_sensor(sensor_id)
    print(f'get sensors: {sensors}')
    if (len(sensors) == 0):
        print(f'no sensors with ID {sensor_id} found, creating new sensor of type {sensor_type}')
        new_sensor(sensor_type, sensor_id)
    return

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

