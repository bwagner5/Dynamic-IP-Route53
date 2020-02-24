# Dynamic-IP-Route53
Updates a Route 53 Zone with your computer's public IP

## Usage:

```
./update_ip.py --help
usage: update_ip.py --zone_name <zone_name> --fqdn <fqdn> --daemon

Update Public IP to Route53

optional arguments:
  -h, --help            show this help message and exit
  --zone_name ZONE_NAME, -z ZONE_NAME
                        Zone Name (i.e. example.com)
  --fqdn FQDN, -f FQDN  Fully Qualified Domain Name (i.e. home.example.com)
  --daemon, -d          Run as a daemon to periodically update the zone (every
                        300 secs)
  --interval INTERVAL, -i INTERVAL
                        Interval in seconds to update IP if run in daemon mode
```

