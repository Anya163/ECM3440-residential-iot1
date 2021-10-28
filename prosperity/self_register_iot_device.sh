echo creating IoT Hub Device
az iot hub device-identity create --device-id soil-moisture-sensor --hub-name anyaiothub

echo retrieving connection string
connection_string=$(az iot hub device-identity connection-string show --device-id soil-moisture-sensor \
 --output table \
 --hub-name <hub_name>)

echo setting IoT Hub connection string environment variable
 export IOT_HUB_CONNECTION_STRING=connection_string

echo starting prosperity app
python3 main.py