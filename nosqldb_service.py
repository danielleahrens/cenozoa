from tinydb import TinyDB, Query

db = TinyDB('db.json')
Sensor = Query()

def new_sensor(sensor_type: str, sensor_id: str):
    # adds new sensor to DB includes sensor_type, sensor_id
    db.insert({'sensor_type': sensor_type, 'sensor_id': sensor_id})
    return

def get_sensor(**kwargs):
    # queries database for sensor given sensor ID or location(s), 
    # returns array of sensors includes the sensor's 
    # location, alert levels and statuses
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
    # updates location field of given sensor ID
    db.update({'location': location}, Sensor.sensor_id == id)
    return

def _get_by_location(locations: list[str]):
    # queries database for sensors given location(s), 
    # returns array of sensors
    resp = []
    for location in locations:
        result = db.search(Sensor.location == location)
        resp = resp + result
    return resp

def _get_by_id(ids: list[str]):
    # queries database for sensors with given id(s),
    # returns array of sensors
    resp = []
    for id in ids:
        result = db.search(Sensor.sensor_id == id)
        resp = resp + result
    return resp

def update_alert(id: str, measurement: str, upper_limit: float, lower_limit: float):
    # updates alert values of sensor given sensor ID
    print(f"id: {id}, measurement: {measurement}, upper limit: {upper_limit}, lower limit: {lower_limit}")
    sensors = get_sensor(ids=id)
    if 'alert' not in sensors[0]:
        db.update({'alert': {measurement: {'upper': upper_limit, 'lower': lower_limit}}}, Sensor.sensor_id == id[0])
        sensors = get_sensor(ids=id)
        print(f'updated first alert: {sensors}')
    else:
        alert = sensors[0]['alert']
        alert[measurement] = {'upper': upper_limit, 'lower': lower_limit}
        db.update({'alert': alert}, Sensor.sensor_id == id[0])
        sensors = get_sensor(ids=id)
        print(f'updated additional alert: {sensors}')
    return

def update_alert_status(id: list, measurement: str, direction: str, alerting: bool):
    sensors = get_sensor(ids=id)
    alert = sensors[0]['alert']
    alert[measurement][direction] = {'limit': sensors[0]['alert'][measurement][direction]['limit'], 'alerting': alerting}
    db.update({'alert': alert}, Sensor.sensor_id == id[0])
    sensors = get_sensor(ids=id)
    print(f"alert updated: {sensors}")
    return

def update_status(id: str, open: bool, heating: bool, watering: bool):
    # updates status values of sensor given sensor ID
    db.update({'status': {'open': open, 'heating': heating, 'watering': watering}}, Sensor.sensor_id == id)
    return


