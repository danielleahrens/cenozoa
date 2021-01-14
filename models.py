
class Metric:
    def __init__(self, sensor_type: str, sensor_id: str, timestamp_ms: int, metric_name: str, metric_value: float, tags: dict):
        self.sensor_type = sensor_type # i.e. batCave
        self.sensor_id = sensor_id # i.e. fruitBat
        self.timestamp_ms = timestamp_ms # i.e. epoch timestamp in millis
        self.metric_name = metric_name # i.e. temperature
        self.metric_value = metric_value # i.e. 42.9
        self.tags = tags # i.e. some additional tags for influx {key: value}
