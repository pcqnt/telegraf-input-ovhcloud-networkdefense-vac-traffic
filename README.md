# telegraf-input-ovhcloud-networkdefense-vac-traffic
Python script to parse the output of [OVHcloud VAC traffic statistics](https://api.ovh.com/console-preview/?section=%2FnetworkDefense&branch=v2#get-/networkDefense/vac/traffic) into the [InfluxDB line protocol](https://docs.influxdata.com/influxdb/latest/reference/syntax/line-protocol/). Intended to be run via Telegraf's [exec](https://github.com/influxdata/telegraf/tree/master/plugins/inputs/exec) input plugin.

## Requirements
OVHcloud Python module (pip install ovh). Other requirements are listed in requirements.txt.

## Install
Configure Telegraf as shown below. Make sure to have the following environnement variables set:
```
OVH_APP_KEY
OVH_APP_SECRET
OVH_CONSUMER_KEY
```
These can be generated on [OVHcloud's portal](https://help.ovhcloud.com/csm/en-gb-api-getting-started-ovhcloud-api?id=kb_article_view&sysparm_article=KB0042784#advanced-usage-pair-ovhcloud-apis-with-an-application).
If needed you can build a docker container with the provided Dockerfile.

## Configuration

`/etc/telegraf/telegraf.conf`
```
[[inputs.exec]]
   commands = ["python3 /usr/src/app/vac-traffic.py 192.0.2.1/32 198.51.100.1/32"]
   data_format = "influx"
   interval = "1h"
   timeout = "600s"

```

## Sample output for two IP Addresses
```
$ python3 ./vac-traffic.py 192.0.2.1/32 198.51.100.1/32
ovh-vac-traffic,subnet=192.0.2.1/32 bps_passed=147733,bps_dropped=0,pps_passed=260,pps_dropped=0 1704274200000000000
ovh-vac-traffic,subnet=192.0.2.1/32 bps_passed=141733,bps_dropped=0,pps_passed=260,pps_dropped=0 1704274500000000000
ovh-vac-traffic,subnet=192.0.2.1/32 bps_passed=143733,bps_dropped=0,pps_passed=260,pps_dropped=0 1704274800000000000
ovh-vac-traffic,subnet=192.0.2.1/32 bps_passed=13733,bps_dropped=0,pps_passed=260,pps_dropped=0 1704275100000000000
ovh-vac-traffic,subnet=192.0.2.1/32 bps_passed=147733,bps_dropped=0,pps_passed=260,pps_dropped=0 1704275400000000000
ovh-vac-traffic,subnet=192.0.2.1/32 bps_passed=117433,bps_dropped=0,pps_passed=260,pps_dropped=0 1704275700000000000
ovh-vac-traffic,subnet=198.51.100.1/32 bps_passed=127733,bps_dropped=0,pps_passed=260,pps_dropped=0 1704276000000000000
ovh-vac-traffic,subnet=198.51.100.1/32 bps_passed=147733,bps_dropped=0,pps_passed=260,pps_dropped=0 1704276300000000000
ovh-vac-traffic,subnet=198.51.100.1/32 bps_passed=137733,bps_dropped=0,pps_passed=260,pps_dropped=0 1704276600000000000
ovh-vac-traffic,subnet=198.51.100.1/32 bps_passed=147733,bps_dropped=0,pps_passed=260,pps_dropped=0 1704276900000000000
ovh-vac-traffic,subnet=198.51.100.1/32 bps_passed=47733,bps_dropped=0,pps_passed=240,pps_dropped=0 1704277200000000000
ovh-vac-traffic,subnet=198.51.100.1/32 bps_passed=147733,bps_dropped=0,pps_passed=260,pps_dropped=0 1704277500000000000

```
## Dashboard

Example Influxdbv2 output configuration in telegraf : 
```
[[outputs.influxdb_v2]]
   urls = ["http://influxdb:8086"]
   token = "redacted"
   organization = "ovh"
   bucket = "network-poll"
```
