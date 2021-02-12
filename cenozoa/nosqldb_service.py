from tinydb import TinyDB, Query
from config import config

db = TinyDB(config.app['db_path'])
Sensor = Query()

def new_sensor(sensor_type: str, sensor_id: str):
    db.insert({'sensor_type': sensor_type, 'sensor_id': sensor_id})
    return

def get_sensor(**kwargs):
    ids = kwargs.get('ids', None)
    locations = kwargs.get('locations', None)
    if (locations is not None and len(locations) > 0):
        resp = _get_by_location(locations)
    elif (ids is not None and len(ids) > 0):
        resp = _get_by_id(ids)
    else:
        resp = db.all()
    return resp

def update_location(id: str, location: str):
    db.update({'location': location}, Sensor.sensor_id == id)
    return

def _get_by_location(locations: list[str]):
    resp = []
    for location in locations:
        result = db.search(Sensor.location == location)
        resp = resp + result
    return resp

def _get_by_id(ids: list[str]):
    resp = []
    for id in ids:
        result = db.search(Sensor.sensor_id == id)
        resp = resp + result
    return resp

def update_alert(id: str, measurement: str, upper_limit: float, lower_limit: float):
    sensors = get_sensor(ids=id)
    if 'alert' not in sensors[0]:
        db.update({'alert': {measurement: {'upper': upper_limit, 'lower': lower_limit}}}, Sensor.sensor_id == id[0])
    else:
        alert = sensors[0]['alert']
        alert[measurement] = {'upper': upper_limit, 'lower': lower_limit}
        db.update({'alert': alert}, Sensor.sensor_id == id[0])
    return

def update_alert_status(id: list, measurement: str, direction: str, alerting: bool):
    sensors = get_sensor(ids=id)
    alert = sensors[0]['alert']
    alert[measurement][direction] = {'limit': sensors[0]['alert'][measurement][direction]['limit'], 'alerting': alerting}
    db.update({'alert': alert}, Sensor.sensor_id == id[0])
    return

def update_status(id: str, open: bool, heating: bool, watering: bool):
    db.update({'status': {'open': open, 'heating': heating, 'watering': watering}}, Sensor.sensor_id == id)
    return


