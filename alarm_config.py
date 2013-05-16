# These alarms are created for each URL that we monitor
HTTP_ALARMS = [
    {
        "namespace": "HTTP",
        "metric_name": "StatusCheckFailed",
        "alarm": {
            "name": "%s IS DOWN",
            "comparison": ">",
            "threshold": "0",
            "period": "300",
            "evaluation_periods": "3",
            "statistic": "Minimum",
            "actions": [
                "arn:aws:sns:us-east-1:615594547923:NotifyMe",
                "arn:aws:sns:us-east-1:615594547923:emergency-notify"
            ],
            "description": "Can't load this URL"
        }
    },
]

# These alarms are created for each instance if the metric is available
INSTANCE_ALARMS = [
    {
        "namespace": "AWS/EC2",
        "metric_name": "StatusCheckFailed",
        "alarm": {
            "name": "%s: INACCESSIBLE",
            "comparison": ">",
            "threshold": "0",
            "period": "300",
            "evaluation_periods": "1",
            "statistic": "Minimum",
            "actions": [
                "arn:aws:sns:us-east-1:615594547923:NotifyMe",
                "arn:aws:sns:us-east-1:615594547923:emergency-notify"
            ],
            "description": "Server is not accessible"
        }
    },
    {
        "namespace": "AWS/EC2",
        "metric_name": "CPUUtilization",
        "alarm": {
            "name": "%s: CPU HIGH",
            "comparison": ">=",
            "threshold": "95",
            "period": "300",
            "evaluation_periods": "3",
            "statistic": "Average",
            "actions": ["arn:aws:sns:us-east-1:615594547923:NotifyMe"],
            "description": "Server is running hot"
        }
    },
    {
        "namespace": "System/Linux",
        "metric_name": "DiskSpaceAvailable",
        "alarm": {
            "name": "%s: DISK SPACE LOW",
            "comparison": "<",
            "threshold": "1.0",
            "period": "300",
            "evaluation_periods": "6",
            "statistic": "Average",
            "actions": ["arn:aws:sns:us-east-1:615594547923:NotifyMe"],
            "description": "Less than 1GB disk space available"
        }
    },
    {
        "namespace": "System/Linux",
        "metric_name": "MemoryUtilization",
        "alarm": {
            "name": "%s: LOW MEMORY",
            "comparison": ">",
            "threshold": "90",
            "period": "300",
            "evaluation_periods": "3",
            "statistic": "Average",
            "actions": [
                "arn:aws:sns:us-east-1:615594547923:NotifyMe",
            ],
            "description": "There is little free memory left"
        }
    },
    {
        "namespace": "Varnish",
        "metric_name": "backend_fail",
        "alarm": {
            "name": "%s: VARNISH BACKEND FAILED",
            "comparison": ">",
            "threshold": "0",
            "period": "300",
            "evaluation_periods": "3",
            "statistic": "Average",
            "actions": [
                "arn:aws:sns:us-east-1:615594547923:NotifyMe",
            ],
            "description": "Varnish is failing to connect to a backend"
        }
    },
    {
        "namespace": "Varnish",
        "metric_name": "fetch_failed",
        "alarm": {
            "name": "%s: VARNISH FETCH FAILED",
            "comparison": ">",
            "threshold": "0",
            "period": "300",
            "evaluation_periods": "3",
            "statistic": "Average",
            "actions": [
                "arn:aws:sns:us-east-1:615594547923:NotifyMe",
            ],
            "description": "Varnish requests to fetch from a backend are failing"
        }
    },
    {
        "namespace": "Varnish",
        "metric_name": "StatusCheckFailed",
        "alarm": {
            "name": "%s: VARNISH FAILURE",
            "comparison": ">",
            "threshold": "0",
            "period": "300",
            "evaluation_periods": "3",
            "statistic": "Average",
            "actions": [
                "arn:aws:sns:us-east-1:615594547923:NotifyMe",
                "arn:aws:sns:us-east-1:615594547923:emergency-notify"
            ],
            "description": "Varnish seems to be down"
        }
    },
    {
        "namespace": "Nginx",
        "metric_name": "StatusCheckFailed",
        "alarm": {
            "name": "%s: NGINX FAILURE",
            "comparison": ">",
            "threshold": "0",
            "period": "300",
            "evaluation_periods": "3",
            "statistic": "Average",
            "actions": [
                "arn:aws:sns:us-east-1:615594547923:NotifyMe",
                "arn:aws:sns:us-east-1:615594547923:emergency-notify"
            ],
            "description": "Nginx seems to be down"
        }
    }
]
