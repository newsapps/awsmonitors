#!/usr/bin/env python

import os
import re
import subprocess
import sys
from urllib2 import urlopen

import settings

import boto.ec2.cloudwatch
c = boto.ec2.cloudwatch.connect_to_region('us-east-1')


def main():
    result = subprocess.Popen(['varnishstat', '-1'], stdout=subprocess.PIPE).communicate()[0]

    if not result:
        print 'status error Varnish is not running.'
        push_metric('StatusCheckFailed', 1)
        sys.exit()

    data = []
    old_data = {}
    new_data = {}

    if os.path.exists(settings.CACHE_FILE):
        with open(settings.CACHE_FILE, 'r') as f:
            for l in f.readlines():
                parts = l.strip().split(',')
                old_data[parts[0]] = int(parts[1])

    try:
        for r in result.split('\n'):
            if not r:
                continue

            parts = re.split('\s+', r.strip())

            if parts[0] in settings.INCLUDE_METRICS:
                if parts[0] in settings.CALCULATE_CHANGE:
                    new_data[parts[0]] = int(parts[1])
                    if parts[0] in old_data:
                        data.append((
                            parts[0],
                            int(parts[1]) - int(old_data[parts[0]]),
                            'Count'))
                else:
                    data.append((parts[0], int(parts[1]), 'Count'))

        if 'cache_hit' in old_data and 'cache_miss' in old_data:
            delta_hits = new_data['cache_hit'] - old_data['cache_hit']
            delta_misses = new_data['cache_miss'] - old_data['cache_miss']

            if delta_misses == 0:
                hit_rate = float(1.0)
            else:
                hit_rate = float(delta_hits) / (delta_hits + delta_misses)

            data.append(('hit_rate', hit_rate, 'Percent'))

    except Exception, e:
        print e
        print 'status warn Error parsing varnishstat output.'
        push_metric('StatusCheckFailed', 1)
        sys.exit()

    print 'status ok Varnish is running.'
    push_metric('StatusCheckFailed', 0)

    with open(settings.CACHE_FILE, 'w') as f:
        f.write('\n'.join([k+','+str(v) for k, v in new_data.items()]))

    for d in data:
        #print d
        push_metric(*d)


def push_metric(key, value, unit=None):
    c.put_metric_data(
        'Varnish',
        key,
        value=value,
        unit=unit,
        dimensions={"InstanceId": get_instance_id()})


def get_instance_id():
    if settings.DEBUG:
        return 'i-7bb79118'

    fp = urlopen('http://169.254.169.254/latest/meta-data/instance-id')
    data = fp.read()
    fp.close()
    return data


if __name__ == '__main__':
    main()
