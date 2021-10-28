# ECM3440-residential-iot1

## IoT DevOps workshop 1

In this first session we will set up a simple Azure IoT project and start preparing a CI/CD pipeline using GitHub and Travis-CI

The IoT example project is taken from <https://github.com/microsoft/IoT-For-Beginners/>

### VS Code

In the VS Code IDE install the Azure IoT Tools extension.  This is a collection of addons that simplifies working with Azure IoT features.

Make sure you also have the Python extension installed too.

### Azure IoT Hub

Create an IoT hub using the Azure portal. <https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-create-through-portal>   Be sure to select the **Free Tier** in the management screen.

You can do this from the command line, see <https://github.com/microsoft/IoT-For-Beginners/blob/main/2-farm/lessons/4-migrate-your-plant-to-the-cloud/README.md>

Rather than install the Azure CLI you might prefer to use the Cloud Shell in the Azure Portal.

### CounterFit

Install the CounterFit IoT sensor simulator. <https://github.com/ExeterBScDTS/CounterFit>

```sh
cd soil-moisture sensor
python3 -m pip install -r requirements.txt
```

Check that it is installed correctly.

```sh
python3 -m CounterFit
```
(or) python -m CounterFit

Quit by typing CRTL-C in the terminal.

### Soil moisture sensor virtual sensor

Before you can use the virtual sensor (or a real sensor if you have the hardware) you need a
connection string.  This is like the string you would use to connect to a database.

See <https://github.com/microsoft/IoT-For-Beginners/blob/main/2-farm/lessons/4-migrate-your-plant-to-the-cloud/README.md> for full details.

In the Cloud Shell you can create an identity for your device with.

```sh
az iot hub device-identity create --device-id soil-moisture-sensor --hub-name <hub_name>
```

Then get the connection string with.

```sh
az iot hub device-identity connection-string show --device-id soil-moisture-sensor \
 --output table \
 --hub-name <hub_name>
```

Copy the string into ```app.py```

Now start CounterFit and add a soil moisture sensor.  See  <https://github.com/microsoft/IoT-For-Beginners/blob/main/2-farm/lessons/2-detect-soil-moisture/virtual-device-soil-moisture.md>

And now run ```app.py```

### Check for messages in the IoT hub

Use the Azure Cloud Shell to see the messages being received.

```
az iot hub monitor-events --hub-name <hub_name>
```

### Did it work?

If it did, then the next thing to do is create your own project repository.

If it didn't, fix it!
