#!/usr/bin/env python

import settings
import alarm_config

import boto.ec2.cloudwatch
import boto.ec2


if __name__ == '__main__':
    c = boto.ec2.cloudwatch.connect_to_region('us-east-1')

    for url in settings.CHECK_URLS:
        for a in alarm_config.HTTP_ALARMS:
            metrics = c.list_metrics(
                dimensions={'URL': url},
                metric_name=a['metric_name'],
                namespace=a.get('namespace', None)
            )
            if not metrics:
                print "No metric '%s:%s' for '%s'" % (
                    a['namespace'], a['metric_name'], url)
            elif len(metrics) > 1:
                print "More than one metric by the name '%s'" % a['metric_name']
            else:
                # Should only have one matching metric for this instance
                m = metrics[0]

                # Generate the name for this alarm
                alarm_name = a['alarm']['name'] % url

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
