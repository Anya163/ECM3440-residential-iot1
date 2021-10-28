from ..components import sensor
from unittest.mock import patch
from mockito import when, unstub
from azure.iot.device import IoTHubDeviceClient, MethodResponse
from counterfit_shims_grove.adc import ADC
import json
from counterfit_connection import CounterFitConnection


@patch.object(IoTHubDeviceClient, 'create_from_connection_string')
@patch.object(IoTHubDeviceClient, 'connect')
def test_succesful_iot_hub_connection(connect, create_from_connection_string):
    #  mock connection string
    create_from_connection_string.return_value = IoTHubDeviceClient
    connect.return_value = IoTHubDeviceClient

    client = sensor.iot_hub_connection()
    print(f'Connected: {client.connected}')
    assert client is IoTHubDeviceClient
    unstub()


def test_unsuccesful_iot_hub_connection():
    client = sensor.iot_hub_connection()
    assert client is None
    unstub()


def test_null_return_from_adc():
    when(sensor).read_adc(IoTHubDeviceClient).thenReturn(None)
    sensor.read_adc(IoTHubDeviceClient)
    assert sensor.read_adc(IoTHubDeviceClient) is None
    unstub()


@patch.object(ADC, 'read')
def test_successful_read_from_adc(read):
    device_client = IoTHubDeviceClient
    read.return_value = 2
    sensor.read_adc(device_client)
    assert sensor.read_adc(IoTHubDeviceClient) == 2
    unstub()


def test_unsuccessful_read_from_adc():
    sensor.read_adc(IoTHubDeviceClient)
    assert sensor.read_adc(IoTHubDeviceClient) is None


@patch.object(IoTHubDeviceClient, 'send_message')
@patch.object(json, 'dumps')
def test_successful_send_message(send_message, dumps):
    device_client = IoTHubDeviceClient
    dumps.return_value = None
    sensor.send_iot_message(2, device_client)
    assert sensor.send_iot_message(2, IoTHubDeviceClient) is None
    unstub()


def test_unsuccessful_send_message():
    device_client = IoTHubDeviceClient
    sensor.send_iot_message(2, device_client)
    assert sensor.send_iot_message(2, IoTHubDeviceClient) is None
    unstub()


@patch.object(CounterFitConnection, 'init')
def test_successful_counterfit_connection(init):
    init.return_value = None
    sensor.counterfit_connection()
    assert sensor.counterfit_connection() is None
    unstub()


def test_unsuccessful_counterfit_connection():
    sensor.counterfit_connection()
    assert sensor.counterfit_connection() is None
    unstub()


@patch.object(MethodResponse, 'create_from_method_request')
@patch.object(IoTHubDeviceClient, 'send_method_response')
def test_successful_handle_request_method(create_from_method_request,
                                          send_method_response):
    create_from_method_request.return_value = None
    send_method_response.return_value = "Test Method Response"

    class test_request:
        name = "Test"

    sensor.handle_method_request(test_request, IoTHubDeviceClient)
    assert sensor.handle_method_request(test_request,
                                        IoTHubDeviceClient) is None


@patch.object(MethodResponse, 'create_from_method_request')
def test_unsuccessful_handle_request_method(create_from_method_request):
    create_from_method_request.return_value = None

    class test_request:
        name = "Test"

    sensor.handle_method_request(test_request, IoTHubDeviceClient)
    assert sensor.handle_method_request(test_request,
                                        IoTHubDeviceClient) is None
