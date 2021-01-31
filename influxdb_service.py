from influxdb import InfluxDBClient
from config import config

influx_client = InfluxDBClient(host=config.influx['host'], port=config.influx['port'])
influx_client.switch_database(config.influx['database'])

def __init__():
    pass

def write_data(json_body):
    resp = influx_client.write_points(json_body, time_precision='s')
    return resp

def read_data(query):
    resp = influx_client.query(query)
    return resp