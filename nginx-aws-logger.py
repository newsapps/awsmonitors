#!/usr/bin/env python

import os
import re
import subprocess
import sys
from urllib2 import urlopen

import settings

import boto.ec2.cloudwatch
c = boto.ec2.cloudwatch.connect_to_region('us-east-1')

if settings.DEBUG:
    instance_id = 'i-7bb79118'
else:
    fp = urlopen('http://169.254.169.254/latest/meta-data/instance-id')
    instance_id = fp.read()
    fp.close()


def main():
    try:
        wp = urlopen('http://localhost:8000/nginx_status')
        result = wp.read()
        wp.close()
    except Exception, ex:
        result = None

    if not result:
        print 'Cannot connect to nginx'
        push_metric('StatusCheckFailed', 1)
        sys.exit()

    data = []
    old_data = {}
    new_data = {}

    if os.path.exists(settings.NGINX_CACHE_FILE):
        with open(settings.NGINX_CACHE_FILE, 'r') as f:
            for l in f.readlines():
                parts = l.strip().split(',')
                old_data[parts[0]] = int(parts[1])

    # process status output
    try:
        for r in result.split('\n'):
            if not r:
                continue

            match = re.match(r'^Active connections: (\d+)$', r.strip())
            if match:
                new_data['ActiveConnections'] = int(match.group(1))
                data.append((
                    'ActiveConnections',
                    int(match.group(1)),
                    'Count'))
                continue

            match = re.match(r'^(\d+)\s+(\d+)\s+(\d+)$', r.strip())
            if match:
                new_data['AcceptedConnections'] = int(match.group(1))
                if 'AcceptedConnections' in old_data:
                    data.append((
                        'AcceptedConnections',
                        int(match.group(1)) - int(old_data['AcceptedConnections']),
                        'Count'))

                new_data['HandledConnections'] = int(match.group(2))
                if 'HandledConnections' in old_data:
                    data.append((
                        'HandledConnections',
                        int(match.group(2)) - int(old_data['HandledConnections']),
                        'Count'))

                new_data['Requests'] = int(match.group(3))
                if 'Requests' in old_data:
                    data.append((
                        'Requests',
                        int(match.group(3)) - int(old_data['Requests']),
                        'Count'))
                continue

            match = re.match(r'^Reading:\s+(\d+)\s+Writing:\s+(\d+)\s+Waiting:\s+(\d+)$', r.strip())
            if match:
                new_data['ConnectionReading'] = int(match.group(1))
                data.append((
                    'ConnectionReading', int(match.group(1)), 'Count'))
                new_data['ConnectionWriting'] = int(match.group(2))
                data.append((
                    'ConnectionWriting', int(match.group(2)), 'Count'))
                new_data['ConnectionWaiting'] = int(match.group(3))
                data.append((
                    'ConnectionWaiting', int(match.group(3)), 'Count'))
                continue

    except Exception, e:
        print e
        print 'status warn Error parsing varnishstat output.'
        push_metric('StatusCheckFailed', 1)
        sys.exit()

    print 'status ok Nginx is running.'
    push_metric('StatusCheckFailed', 0)

    with open(settings.NGINX_CACHE_FILE, 'w') as f:
        f.write('\n'.join([k+','+str(v) for k, v in new_data.items()]))

    for d in data:
        print d
        push_metric(*d)


def push_metric(key, value, unit=None):
    c.put_metric_data(
        'Nginx',
        key,
        value=value,
        unit=unit,
        dimensions={"InstanceId": instance_id})


if __name__ == '__main__':
    main()
