awsmonitors
===========

Cron scripts that report metric data to Amazon CloudWatch

These scripts are meant to be run by cron on ec2 servers every 5 minutes.

## Varnish

Use the `varnish-aws-logger.py` to report `varnishstat	` data to Amazon. Rolls into the 'Varnish' namespace and associates the metrics with the instance id of the machine it's run on.

Look at the `settings.py` file to configure what metrics you want sent to AWS.

## Nginx

Use the `nginx-aws-logger.py` to report nginx status data to Amazon. Rolls into the 'Nginx' namespace and associates the metrics with the instance id of the machine it's run on.

You have to make sure you have	 the following in your nginx config:

	server {
		listen 127.0.0.1:8000;
	
		location /nginx_status {
			# copied from http://blog.kovyrin.net/2006/04/29/monitoring-nginx-with-rrdtool/
			stub_status on;
			access_log   off;
			allow 127.0.0.1;
			deny all;
		}
	}

## Deploying

Deployment is handled through Fabric. *Do not save server information in the fabfile!*

To setup a new server:

	fab setup -H ec2-x-x-x-x.compute-x.amazonaws.com -u myusername

To update these scripts on a server:

	fab update -H ec2-x-x-x-x.compute-x.amazonaws.com -u myusername

To install the crontab on a server:

	fab install_cron:crontab-na-varnish -H ec2-x-x-x-x.compute-x.amazonaws.com -u myusername

For the `install_cron` command, you need to create a `crontab-creds` file. Copy the `crontab-creds.example` to `crontab-creds` and fill in the AWS values. The `install_cron` command takes an argument which is the name of the crontab file to install from the root of this repo.
