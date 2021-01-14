from models import Metric

class MetricService:
    def __init__(self):
        pass

    def create(self, metric_request):
        print(metric_request)
        metric = Metric(
            sensor_type = metric_request['sensor_type'], 
            sensor_id = metric_request['sensor_id'], 
            timestamp_ms = metric_request['timestamp_ms'], 
            metric_name = metric_request['metric_name'], 
            metric_value = metric_request['metric_value'], 
            tags = metric_request['tags']
        )
        statsd_str = f"cenozoa.metrics,sensor_type={metric.sensor_type},sensor_id={metric.sensor_id},time={metric.timestamp_ms},{metric.metric_name}={metric.metric_value}"
