import time
import json
import os
import logging
from dotenv import load_dotenv
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse
from counterfit_shims_grove.adc import ADC
from counterfit_shims_grove.grove_relay import GroveRelay
from counterfit_connection import CounterFitConnection

load_dotenv()
# Extract environment variables into Python variables.
# Now these don't need to be changed for each environment.
COUNTERFIT_HOST = os.getenv('COUNTERFIT_HOST')
COUNTERFIT_PORT = os.getenv('COUNTERFIT_PORT')

# SENSOR_TYPE, SENSOR_NAME and GPIO pin have been environmentalised
# so that sensor.py can be reused to represent any kind of virtual sensor
SENSOR_NAME = os.getenv('SENSOR_NAME')
SENSOR_TYPE = os.getenv('SENSOR_TYPE')
GPIO_PIN = os.getenv('GPIO_PIN')
RELAY_PIN = os.getenv('RELAY_PIN')

IOT_HUB_CONNECTION_STRING = os.getenv('IOT_HUB_CONNECTION_STRING')


# Virtual Analog-to-Digital Converter
adc = ADC()
relay = GroveRelay(RELAY_PIN)


# Establish connection with CounterFit App
def counterfit_connection():
    try:
        CounterFitConnection.init(COUNTERFIT_HOST, COUNTERFIT_PORT)
    except Exception as counterfit_exception:
        logging.info("CounterFit Connection not Established." +
                     counterfit_exception)


# Establish connection with Azure IoT Hub
def iot_hub_connection():
    device_client = None
    try:
        device_client = IoTHubDeviceClient.\
            create_from_connection_string(IOT_HUB_CONNECTION_STRING)
        print('Connecting')
        device_client.connect()
        print('Connected')

    except Exception as iot_hub_exception:
        logging.info("IoT Hub Connection not Established." +
                     iot_hub_exception)

    return device_client


def handle_method_request(request, device_client):
    print("Direct method received - ", request.name)

    if request.name == "relay_on":
        relay.on()
    elif request.name == "relay_off":
        relay.off()

    try:
        method_response = MethodResponse.\
            create_from_method_request(request, 200)
        device_client.send_method_response(method_response)
    except Exception as method_response_exception:
        logging.info("Method Response Could Not Be Established." +
                     method_response_exception)


# Read values from virtual sensor.
def read_adc(device_client):
    soil_moisture = None
    try:
        soil_moisture = adc.read(GPIO_PIN)
        print("Soil moisture:", soil_moisture)
    except Exception as soil_moisture_exception:
        logging.info("Sensor Could Not Be Read." + soil_moisture_exception)

    return soil_moisture


def send_iot_message(soil_moisture, device_client):
    try:
        message = Message(json.dumps({'soil_moisture': soil_moisture}))
        device_client.send_message(message)
    except Exception as send_message_exception:
        logging.info("Data Could Not Be Sent." + send_message_exception)


def run(device_client):
    device_client.on_method_request_received = handle_method_request
    while True:
        soil_moisture = read_adc()
        send_iot_message(soil_moisture, device_client)
        time.sleep(2)
