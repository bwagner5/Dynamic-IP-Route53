#!/usr/bin/env python
import boto3
import time
import configargparse
import requests
import socket


class UpdateIP(object):

    def __init__(self, zone_name, fqdn):
      if zone_name[-1] != '.':
          zone_name = zone_name + '.'
      self.route53_client = boto3.client('route53')
      self.zone_name = zone_name
      self.zone_id = None
      self.fqdn = fqdn

    def is_zone_current(self):
      return self.get_public_ip() == socket.gethostbyname(self.fqdn).strip()

    def update_ip(self):
      zone_id = self.get_zone_id()
      return self.route53_client.change_resource_record_sets(
        HostedZoneId=zone_id,
        ChangeBatch=self.get_record_change(self.fqdn, self.get_public_ip())
      )

    def get_zone_id(self):
      if self.zone_id is not None:
        return self.zone_id
      for zone in self.route53_client.list_hosted_zones()['HostedZones']:
          if zone['Name'] == self.zone_name:
              self.zone_id = zone['Id']
              return zone['Id']
              break

    def get_public_ip(self):
      return requests.get(url = "http://checkip.amazonaws.com").text.strip()

    def get_record_change(self, fqdn, ip):
        return {
                "Comment": "update ip",
                "Changes": [
                  {
                    "Action": "UPSERT",
                    "ResourceRecordSet": {
                      "Name": "%s" % fqdn,
                      "Type": "A",
                      "TTL": 300,
                      "ResourceRecords": [
                        {
                          "Value": "%s" % ip
                        }
                      ]
                    }
                  }
                ]
              }

if __name__ == '__main__':
    parser = configargparse.ArgParser(
        description="Update Public IP to Route53",
        usage='''update_ip.py --zone_name <zone_name> --fqdn <fqdn> --daemon''')
    parser.add('--zone_name', '-z', help="Zone Name (i.e. example.com)", env_var='ZONE_NAME')
    parser.add('--fqdn', '-f', help="Fully Qualified Domain Name (i.e. home.example.com)", env_var='FQDN')
    parser.add('--daemon', '-d', help="Run as a daemon to periodically update the zone (every 300 secs)", action='store_true', env_var='DAEMON')
    parser.add('--interval', '-i', help="Interval in seconds to update IP if run in daemon mode", default=300, type=int, env_var='INTERVAL')
    args = parser.parse_args()
    while True:
      dynamic_dns_updater = UpdateIP(args.zone_name, args.fqdn)
      if not dynamic_dns_updater.is_zone_current():
        print(dynamic_dns_updater.update_ip())
      else:
        print("Zone is current with IP: " + dynamic_dns_updater.get_public_ip())
      if args.daemon:
        time.sleep(args.interval)
      else:
        break
