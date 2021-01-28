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
    id = kwargs.get('id', None)
    locations = kwargs.get('locations', None)
    if (locations is not None and len(locations) > 0):
        resp = _get_location(locations)
    elif (id is not None):
        resp = db.search(Sensor.sensor_id == id)
    else:
        resp = db.all()
    return resp

def update_location(id: str, location: str):
    # updates location field of given sensor ID
    db.update({'location': location}, Sensor.sensor_id == id)
    return

def _get_location(locations: list[str]):
    # queries database for sensors given location(s), 
    # returns array of sensors
    resp = []
    for location in locations:
        result = db.search(Sensor.location == location)
        resp = resp + result
    return resp

def update_alert(id: str, upper_limit: float, lower_limit: float, time: float):
    # updates alert values of sensor given sensor ID
    db.update({'alerts': {'upper': upper_limit, 'lower': lower_limit, 'time': time}}, Sensor.sensor_id == id)
    return

def update_status(id: str, open: bool, heating: bool, watering: bool):
    # updates status values of sensor given sensor ID
    db.update({'statuses': {'open': open, 'heating': heating, 'watering': watering}}, Sensor.sensor_id == id)
    return


