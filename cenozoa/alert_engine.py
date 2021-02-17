from config import config
from nosqldb_service import get_sensor, update_alert_status
from influxdb_service import read_data
from alert_service import check_upper_alert_status, check_lower_alert_status, send_alert
from server import find_min_and_max

import time


def check_alerting():
    time_range = int((time.time() - 330) * 1000000000) # 330 seconds in 5.5 minutes, convert seconds to nanoseconds
    sensors = get_sensor()
    for sensor in sensors:
        if 'alert' not in sensor.keys():
            continue
        for measurement in sensor['alert'].keys():
            query = f"SELECT time, value, sensor_id, units FROM {measurement} where time > {time_range} and sensor_id = \'{sensor['sensor_id']}\' ORDER BY time desc"
            metrics = read_data(query).raw['series']
            if len(metrics) == 0:
                continue

            max_metric, min_metric = find_min_and_max(metrics[0]['values'])
            upper_alert_status_update = check_upper_alert_status(max_metric, sensor['alert'][measurement]['upper']['limit'], sensor['alert'][measurement]['upper']['alerting'])
            if upper_alert_status_update is not None:
                update_alert_status([sensor['sensor_id']], measurement, 'upper', upper_alert_status_update)
                if upper_alert_status_update == 'True':
                    msg_high = f"ALERT: sensor {sensor['sensor_id']} is alerting for {measurement} too high. Current measurement: {max_metric}; Alert limit: {sensor['alert'][measurement]['upper']['limit']}"
                elif upper_alert_status_update == 'False':
                    msg_high = f"OK: sensor {sensor['sensor_id']} is no longer alerting for {measurement} too high. Current measurement: {max_metric}; Alert limit: {sensor['alert'][measurement]['upper']['limit']}"
                send_alert({"text": msg_high}, config.alert['url'])
            
            lower_alert_status_update = check_lower_alert_status(min_metric, sensor['alert'][measurement]['lower']['limit'], sensor['alert'][measurement]['lower']['alerting'])
            if lower_alert_status_update is not None:
                update_alert_status([sensor['sensor_id']], measurement, 'lower', lower_alert_status_update)
                if lower_alert_status_update == 'True':
                    msg_low = f"ALERT: sensor {sensor['sensor_id']} is alerting for {measurement} too low. Current measurement: {min_metric}; Alert limit: {sensor['alert'][measurement]['lower']['limit']}"
                elif lower_alert_status_update == 'False':
                    msg_low = f"OK: sensor {sensor['sensor_id']} is no longer alerting for {measurement} too low. Current measurement: {min_metric}; Alert limit: {sensor['alert'][measurement]['lower']['limit']}"
                send_alert({"text": msg_low}, config.alert['url'])
    
    return 201

if __name__ == "__main__":
    loop = True
    while loop is True:
        print('checking alert statuses')
        resp = check_alerting()
        if resp != 201:
            send_alert({"text": "ALERT: cenozoa experienced an error while updating the alert status of cenozoa sensors."}, config.alert['url'])
        t = time.localtime()
        print(f'{time.strftime("%H:%M:%S", t)} sleeping for 5 minutes.')
        time.sleep(300)