#!/usr/bin/env python

from urllib2 import urlopen, URLError
from time import clock

import settings

import boto.ec2.cloudwatch
c = boto.ec2.cloudwatch.connect_to_region('us-east-1')

for url in settings.CHECK_URLS:
    start = clock()
    try:
        webpage = urlopen(url, timeout=15)
        code = webpage.getcode()
        headers = webpage.info()
        content = webpage.read()
        webpage.close()
        req_time = clock() - start
        del webpage

        if code == 200 and len(content.strip()) > 1:
            success = True
        else:
            success = False
            print code
            print len(content.strip())
            print "Failed %f" % req_time

    except URLError, ex:
        req_time = -1
        success = False
        print ex
        print "Failed %f" % req_time

    c.put_metric_data(
        'HTTP', 'StatusCheckFailed',
        value=0 if success else 1,
        dimensions={"URL": url})

    c.put_metric_data(
        'HTTP', 'ResponseTime',
        value=req_time,
        unit='Seconds',
        dimensions={"URL": url})
