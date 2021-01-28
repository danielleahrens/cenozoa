from tinydb import TinyDB, Query

db = TinyDB('db.json')
Sensor = Query()

def new_sensor(sensor_type: str, sensor_id: str):
    # adds new sensor to DB includes sensor_type, sensor_id
    db.insert({'sensor_type': sensor_type, 'sensor_id': sensor_id})
    return

def get_sensor(id: str):
    # queries database for sensor given sensor ID, 
    # returns array of sensors includes the sensor's 
    # location, alert levels and statuses
    resp = db.search(Sensor.sensor_id == id)
    return resp

def update_location(id: str, location: str):
    # updates location field of given sensor ID
    db.update({'location': location}, Sensor.sensor_id == id)
    return

def get_location(locations: list[str]):
    # queries database for sensors given location(s), 
    # returns array of sensors
    count_location = len(locations)
    if (count_location == 1):
        resp = db.search(Sensor.location == locations[0])
    elif (count_location < 1):
        resp = []
    else:
        query = f'(Sensor.location == '
        for location in locations:
            if (locations[count_location - 1] == location):
                query = query + location + '))'
            else:
                query = query + location + ') | (Sensor.location == '
        print(f'search query: {query}')
        resp = db.search(query)
    return resp

def update_alert(id: str, upper_limit: float, lower_limit: float, time: float):
    # updates alert values of sensor given sensor ID
    db.update({'alerts': {'upper': upper_limit, 'lower': lower_limit, 'time': time}}, Sensor.sensor_id == id)
    return

def update_status(id: str, open: bool, heating: bool, watering: bool):
    # updates status values of sensor given sensor ID
    db.update({'statuses': {'open': open, 'heating': heating, 'watering': watering}}, Sensor.sensor_id == id)
    return


