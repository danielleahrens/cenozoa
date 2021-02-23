# Cenozoa IoT Farm Platform

The Cenozoa IoT Farm is a custom built platform. The vision of this platform is to achieve a network of sensors and automated systems to form a highly connected, fully integrated hobby farm. The platform is designed so that many types of IoT sensors can integrate with the system, sending measurement (i.e. temperature, humidity, light) or status (i.e. watering, heating, open/close) metrics to a server. Through a UI, the sensor metrics can be viewed and additional meta data (i.e. alert limits, location) can be added to enrich each sensor or manual overrides can be set (i.e. stop watering, turn off heat or close door).

Currently one IoT sensor type has been developed: a temperature and humidity monitoring sensor (https://github.com/danielleahrens/batCave). This sensor's primary purpose is to monitor the environmental conditions of various storage locations. Such as a cold, humid root cellar for storing cabbage and root vegetables, a cool, dry root cellar for storing winter squash or a cold, dry root cellar for storing alliums.

The current status and 24 hour highs and lows for each sensor can be viewed in the UI (https://github.com/danielleahrens/attenborough), as well as an expanded, detailed view of the previous week's metrics. The user can add and change a sensor's alert limits and update its location through the UI (no updating firmware when you add a new sensor or move it to a new spot in the house!).

In addition to acting as the primary hub for the sensors and the UI, the Cenozoa web server (https://github.com/danielleahrens/cenozoa) also monitors each sensor's current status and compares it to its alert limits. It fires an alert if a sensor is outside of the allowable range, so that the user can respond accordingly. 

# Cenozoa

![cenozoa_diagram](https://user-images.githubusercontent.com/31782840/108779365-bf1c8a80-7534-11eb-91d8-64da8f6bad4e.png)

This is the web server for the Cenozoa IoT Platform. The component parts incldue:
- Web Server: https://github.com/danielleahrens/cenozoa
- User Interface: https://github.com/danielleahrens/attenborough
- Temp/Humidity Sensor: https://github.com/danielleahrens/batCave

## Config
There are 3 layers of config for this application. First, there is a general config file which includes details for connecting to the Influx database (see below for additional requirements for running this server). In addition, it includes the URL to be added to the CORs headers and the path to the no SQL database (see below for additional requirements for running this server). 

In addition to the application.json file, there is a required secrets.json file which includes the secret URL for the Slack incoming webhooks (see below for additional requirements for running this server).

There are also default config settings which can be used for local development. See the `application.json` file for an example of the config structure.

## Additional Requirements

### InfluxDB
This server utilizes InfluxDB as its datastore for the measurement data received by the IoT sensors. It writes to InfluxDB for each measurement metric it receives from the IoT sensors and reads the data on request from the UI. See the InfluxDB docs to get started: https://docs.influxdata.com/influxdb/v2.0/get-started/ 

### TinyDB
This server also utilizes a no SQL database for storing information about each sensor (i.e. the sensor location, the alert limits for each measurement type, the alert status). A high performance database isn't currently required for this platform, so TinyDB (https://tinydb.readthedocs.io/en/latest/) is being used. It is a very basic, document oriented database that works well in Python projects. See the `db_example.json` file to see an example of the structure and content of this database.

### Slack
This server includes a cron that checks each sensor's recent metrics and compares it to its alert limits (if they exist). If the alert status changes i.e. was alerting, but now is within the upper and lower limits or wasn't alerting but is now outside the upper and lower alert limits, then it will fire a message into a Slack channel. A Slack channel with a custom Slack App and bot user will be required. The App will require permission to post to a Slack channel using a private webhook URL. See these docs for an example of how to set this up: https://api.slack.com/messaging/webhooks.


