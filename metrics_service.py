from models import Metric
from influxdb_service import write_data
import json

class MetricService:
    def __init__(self):
        pass

    def create(self, metric_request):
        metric = Metric(
            sensor_type = metric_request['sensor_type'], 
            sensor_id = metric_request['sensor_id'], 
            timestamp_s = metric_request['timestamp_s'], 
            metric_name = metric_request['metric_name'], 
            metric_value = metric_request['metric_value'], 
            tags = metric_request['tags']
        )
        influx_body = [{
            "measurement": metric.metric_name,
            "tags": {
                "sensor_type": metric.sensor_type,
                "sensor_id": metric.sensor_id
            },
            "time": int(metric.timestamp_s),
            "fields": {
                "Float_value": metric.metric_value
            }
        }]
        print(influx_body)
        write_data(influx_body)
        return 
