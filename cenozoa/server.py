#!/bin/bash

from flask import Flask, Response, request, jsonify
from flask_cors import CORS, cross_origin
from metrics_service import MetricService
from models import Metric
from config import config
from nosqldb_service import new_sensor, get_sensor, update_location, update_alert
from influxdb_service import read_data

import json
import time
import numpy

metric_service = MetricService()

app= Flask(__name__)
CORS(app, resources={r"/*": {"origins": config.app['cors']}})

@app.route("/api/v1/sensor", methods=["GET", "PUT"])
def sensor():
    if request.method == 'GET':
        locations = request.args.getlist('l')
        sensors = get_sensor(locations=locations)
        response = jsonify(items=sensors)
        response.headers.add("Access-Control-Allow-Origin", config.app['cors'])
        return response, 201

    if request.method == 'PUT':
        request_obj = request.get_json()
        verify_sensor(request_obj['sensor_type'], request_obj['sensor_id'])
        update_location(request_obj['sensor_id'][0], request_obj['location'])
    return Response(status=201)

@app.route("/api/v1/sensor/metric", methods=["GET", "POST"])
def metric():
    if (request.method == 'GET'):
        time_range = int((time.time() - 86400) * 1000000000) # 86,400 seconds in 24 hours, convert seconds to nanoseconds
        locations = request.args.getlist('l')
        sensors = get_sensor(locations=locations)
        measurements = read_data('SHOW measurements')
        measurements = measurements.raw['series'][0]['values']
        i = 0
        for sensor in sensors:
            for measurement in measurements:
                query = f"SELECT time, value, sensor_id, units FROM {measurement[0]} where time > {time_range} and sensor_id = \'{sensor['sensor_id']}\' ORDER BY time desc"
                data = read_data(query)
                if len(data.raw['series']) > 0:
                    data_points = data.raw['series'][0]['values']
                    highest_measurement, lowest_measurement = find_min_and_max(data_points)
                    current_measurement = float(data_points[0][1]) # data values are listed in time, value, id order.
                            
                    if 'measurement' not in sensor:
                        sensor['measurement'] = {measurement[0]: {'current': current_measurement, 'high': highest_measurement, 'low': lowest_measurement, 'uom': data_points[0][3]}}
                    else:
                        sensor['measurement'][measurement[0]] = {'current': current_measurement, 'high': highest_measurement, 'low': lowest_measurement, 'uom': data_points[0][3]}
            sensors[i] = sensor
            i = i + 1
        response = jsonify(items=sensors)
        return response, 201
    
    if request.method == 'POST':
        request_obj = request.get_json()
        verify_sensor(request_obj['sensor_type'], list(request_obj['sensor_id']))
        sensor = get_sensor(ids=request_obj['sensor_id'])
        try:
            location = sensor[0]['location']
            tags = request_obj['tags'] + [{'location': location}]
            request_obj['tags'] = tags
        except:
            print(f'sensor {sensor[0]["sensor_id"]} has no location associated with it, not adding to tags.')
        try:
            status = sensor[0]['status']
            tags = request_obj['tags'] + [{'status': status}]
            request_obj['tags'] = tags
        except:
            print(f'sensor {sensor[0]["sensor_id"]} has no status associated with it, not adding to tags')
        request_obj['sensor_id'] = request_obj['sensor_id'][0]
        resp = metric_service.create(request_obj)
        return Response(status=201)

@app.route("/api/v1/sensor/metric/detail", methods=["GET"])
def detail():
    if request.method == 'GET':
        time_range = int((time.time() - 604800) * 1000000000) # 604,800 seconds in 1 week, convert seconds to nanoseconds
        sensor_id = request.args.getlist('s')
        sensors = get_sensor(ids=sensor_id)
        measurements = read_data('SHOW measurements')
        measurements = measurements.raw['series'][0]['values']
        i = 0
        for sensor in sensors:
            for measurement in measurements:
                query = f"SELECT LAST(time), MEAN(value), LAST(sensor_id) FROM {measurement[0]} where time > {time_range} and sensor_id = \'{sensor['sensor_id']}\' GROUP BY time(30m) ORDER BY time desc"
                data = read_data(query)
                if len(data.raw['series']) > 0:
                    data_points = data.raw['series'][0]['values']
                    if 'measurement' not in sensor:
                        sensor['measurement'] = {measurement[0]: data_points}
                    else:
                        sensor['measurement'][measurement[0]] = data_points
            sensors[i] = sensor
            i = i + 1
    response = jsonify(items=sensors) 
    return response, 201

@app.route("/api/v1/sensor/metric/alert", methods=["PUT"])
@cross_origin()
def alert():
    if request.method == 'PUT':
        request_obj = request.get_json()
        verify_sensor(request_obj['sensor_type'], request_obj['sensor_id'])
        for measurement in request_obj['alert'].keys():
            update_alert(
                request_obj['sensor_id'], 
                measurement, 
                request_obj['alert'][measurement]['upper'], 
                request_obj['alert'][measurement]['lower'], 
            )
    return Response(status=201)

def verify_sensor(sensor_type, sensor_id: list):
    sensors = get_sensor(ids=sensor_id)
    if len(sensors) == 0:
        print(f'no sensors with ID {sensor_id[0]} found, creating new sensor of type {sensor_type}')
        new_sensor(sensor_type, sensor_id[0])
    return

def find_min_and_max(data_pts):
    max_metric = data_pts[0][1]
    min_metric = data_pts[0][1]
    
    for metric in data_pts:
        if float(metric[1]) > float(max_metric):
            max_metric = metric[1]
        elif float(metric[1]) < float(min_metric):
            min_metric = metric[1]
            
    return max_metric, min_metric

if __name__ == "__main__":
    app.run(debug=True if config.app['debug'] == 'True' else False, host='0.0.0.0')

