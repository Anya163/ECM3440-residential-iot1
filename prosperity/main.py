import logging
from components.sensor import counterfit_connection, iot_hub_connection, run

# Set up logger
logging.basicConfig(
    format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
logging.info('Starting up the app...')

if __name__ == "__main__":
    # connecting to counterfit
    counterfit_connection()

    # setting up device client
    device_client = iot_hub_connection()
    if device_client:
        # call run function in sensor.py
        run(device_client)
    else:
        logging.info("Device Client Could Not Be Established. Exiting.")
