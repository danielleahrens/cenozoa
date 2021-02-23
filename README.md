# Cenozoa

![cenozoa_diagram](https://user-images.githubusercontent.com/31782840/108779365-bf1c8a80-7534-11eb-91d8-64da8f6bad4e.png)

This is the web server for the Cenozoa IoT Platform (https://cenozoa.danielleahrens.com). The component parts incldue:
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


