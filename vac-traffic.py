#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import ovh
from os import environ
import logging
import argparse
import sys
import ipaddress
from datetime import datetime, timedelta, timezone
from dateutil.parser import parse

def main():    
    parser = argparse.ArgumentParser(description='OVHcloud VAC Traffic API Poller')
    parser.add_argument('subnet',help='Target IP in format 192.0.2.1/32', type=str, nargs='+')
    parser.add_argument('--hourly',help='Poll for last hour (default)', action='store_true')
    parser.add_argument('--daily',help='Poll for 24 hours', action='store_true')
    parser.add_argument('--weekly',help='Poll for last 7 days', action='store_true')
    parser.add_argument('--measurementname',help="InfluxDB lineformat measurement name, defaults to 'ovh-vac-traffic'",default='ovh-vac-traffic')
    parser.add_argument('--endpoint',help="OVHcloud API endpoint, defaults to 'ovh-eu'", default='ovh-eu')
    parser.add_argument('--verbose',action='store_true')
    args= parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    if args.weekly:
        aftertime=(datetime.now(timezone.utc)-timedelta(days=7)).astimezone().isoformat('T')
    elif args.daily:
        aftertime=(datetime.now(timezone.utc)-timedelta(hours=24)).astimezone().isoformat('T')
    else:
        aftertime=(datetime.now(timezone.utc)-timedelta(hours=1)).astimezone().isoformat('T')

    for subnet in args.subnet:
        try:
            ipaddress.ip_network(subnet)
        except ValueError:
            logging.error('--subnet %s is not an ip network', args.subnet)
            sys.exit()

    client = ovh.Client(
        endpoint=args.endpoint,               # Endpoint of API OVH Europe (List of available endpoints)
        application_key=environ['OVH_APP_KEY'],    # Application Key
        application_secret=environ['OVH_APP_SECRET'], # Application Secret
        consumer_key=environ['OVH_CONSUMER_KEY'],       # Consumer Key
    )

    for subnet in args.subnet:
        logging.info('Now processing subnet:%s',subnet)
        result= client.get('/v2/networkDefense/vac/traffic', after=aftertime, subnet=subnet)
        if 'timestamps' not in result:
            logging.error('Empty API response')
            sys.exit()
        i=0
        for timestamp in result['timestamps']:
            unixtimestamp= parse(timestamp).timestamp()*1000*1000*1000
            print('{},subnet={} bps_passed={},bps_dropped={},pps_passed={},pps_dropped={} {:.0f}'\
                .format(args.measurementname, subnet, \
                        result['bps']['passed'][i], result['bps']['dropped'][i], \
                            result['pps']['passed'][i], result['pps']['dropped'][i], \
                                unixtimestamp))
            i+=1
if __name__ == '__main__':
    main()
