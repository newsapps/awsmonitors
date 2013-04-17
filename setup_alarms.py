#!/usr/bin/env python

import os
import re
import subprocess
import sys
from urllib2 import urlopen, URLError

import settings
import alarm_config

import boto.ec2.cloudwatch
import boto.ec2


def get_servers(filters):

    conn = boto.ec2.connect_to_region('us-east-1')
    reservations = conn.get_all_instances(filters=filters)

    servers = list()
    for r in reservations:
        for i in r.instances:
            s = i.__dict__
            s['security_groups'] = map(lambda x: x.id, r.groups)
            servers.append(s)

    return servers

if __name__ == '__main__':
    c = boto.ec2.cloudwatch.connect_to_region('us-east-1')

    # Get the instance id
    if len(sys.argv) > 1:
        instance_id = sys.argv[1]
    else:
        print "Looking for instance id..."
        try:
            fp = urlopen(
                'http://169.254.169.254/latest/meta-data/instance-id',
                timeout=5)
            instance_id = fp.read()
            fp.close()
        except URLError, ex:
            print "Can't find it - please pass an instance id as the first argument"
            sys.exit()

    for a in alarm_config.ALARMS:
        servers = get_servers({
            'instance-id': instance_id
        })

        for s in servers:
            metrics = c.list_metrics(
                dimensions={'InstanceId': s['id']},
                metric_name=a['metric_name'],
                namespace=a.get('namespace', None)
            )
            if not metrics:
                print "No metric '%s:%s' for '%s'" % (
                    a['namespace'], a['metric_name'], s['tags']['Name'])
            elif len(metrics) > 1:
                print "More than one metric by the name '%s'" % a['metric_name']
            else:
                # Should only have one matching metric for this instance
                m = metrics[0]

                # Generate the name for this alarm
                alarm_name = a['alarm']['name'] % s['tags']['Name']

                # Create or update the alarm
                new_alarm = m.create_alarm(
                    name=alarm_name,
                    comparison=a['alarm']['comparison'],
                    threshold=a['alarm']['threshold'],
                    period=a['alarm']['period'],
                    evaluation_periods=a['alarm']['evaluation_periods'],
                    statistic=a['alarm']['statistic'],
                    description=a['alarm']['description'],
                    alarm_actions=a['alarm']['actions']
                )
                print "Created alarm '%s'" % alarm_name
