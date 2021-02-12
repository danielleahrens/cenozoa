import requests

def send_alert(request_obj: dict, url: str):
    resp = requests.post(url, json=request_obj)
    return resp

def check_upper_alert_status(max_metric: float, upper_limit: float, alert_status: str):
    update_alert_to = None
    if float(max_metric) > float(upper_limit) and alert_status == 'False':
        update_alert_to = "True"
    elif float(max_metric) < float(upper_limit) and alert_status == 'True':
        update_alert_to = "False"
    return update_alert_to

def check_lower_alert_status(min_metric: float, lower_limit: float, alert_status: str):
    update_alert_to = None
    if float(min_metric) < float(lower_limit) and alert_status == 'False':
        update_alert_to = "True"
    elif float(min_metric) > float(lower_limit) and alert_status == 'True':
        update_alert_to = "False"
    return update_alert_to