## A Simple Balena integration with Splunk

This is a simple [Splunk][splunk-link] integration that works with any of the devices supported by [Balena][balena-link].

The main.py script collects OS performance metrics via shell commands and then sends to a specified metrics index on either Splunk Cloud or Splunk Enterprise.

To get this project up and running on the Splunk end, you'll need to have a working [Splunk Cloud][splunk-cloud-trial] or [Splunk Enterprise][splunk-enterprise-trial] environment with the [HTTP Event Collector (HEC)][splunk-hec] enabled and accessible from the internet. You'll also need to create a HEC  authentication token and have a target metrics index enabled.

On the Balena end, signup for a balena account [here][signup-page], set up a device, and have a look at the [Getting Started tutorial][gettingStarted-link]. Once you are set up with balena, you will need to clone this repo locally.

Follow these [steps][push-balena] to push the code to your fleet to enable the data collection. Make sure to change the Dockerfile.template file to match the architecture of the target device for the [build][balena-build].

Once deployed, add the three OS environment variables below to enable the connection to Splunk:

```
SPLUNK_HOST = IP address or hostname of remote Splunk host
```

```
SPLUNK_TOKEN = the Splunk authentication token for HEC access
```

```
SPLUNK_INDEX = the name of the Splunk target index where the data will be stored
```

Note: The Splunk index must be a metrics index (not events).

This is how the variables should look on the Balena console:
![Enable device URL](/img/device_variables.png)

Once running correctly, you should see this in your logs:
![log output](/img/balena_console.png)

Metrics collected include the following:
```
load5min, DiskSize, DiskUsed, DisckUsedPct, UsedMem, TotalMem, UsedMemPct
```
Metrics dimensions (metadata) collected include the following:
```
balena_machine_name, balena_device_type, balena_local_ip
```
Here's an example search in Splunk using the load5min metric:
![splunk_dashboard](/img/splunk_dashboard.png)

[balena-link]:https://balena.io/
[signup-page]:https://dashboard.balena-cloud.com/signup
[gettingStarted-link]:http://balena.io/docs/learn/getting-started/
[splunk-cloud-trial]:https://www.splunk.com/en_us/download/splunk-cloud.html
[splunk-enterprise-trial]:https://www.splunk.com/en_us/download/splunk-enterprise.html
[splunk-hec]:https://docs.splunk.com/Documentation/Splunk/8.2.4/Data/UsetheHTTPEventCollector
[splunk-link]:https://www.splunk.com
[push-balena]:https://www.balena.io/docs/learn/deploy/deployment/
[balena-build]:https://www.balena.io/docs/learn/develop/dockerfile/
