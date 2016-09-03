#!/usr/bin/env python
import boto3
import sys
import time
import subprocess
import argparse


class UpdateIP(object):

    def __init__(self, zone_name, fqdn, cmd):
      if zone_name[-1] != '.':
          zone_name = zone_name + '.'

      self.route53_client = boto3.client('route53')

      for zone in self.route53_client.list_hosted_zones()['HostedZones']:
          if zone['Name'] == zone_name:
              self.zoneId = zone['Id']
              break

      print self.route53_client.change_resource_record_sets(
        HostedZoneId=self.zoneId,
        ChangeBatch=self.getRecordChange(fqdn, self.getPublicIP(cmd))
     )


    def getPublicIP(self):
      return subprocess.check_output(['/bin/bash', '-c', cmd])

    def getRecordChange(self, fqdn, ip):
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
    parser = argparse.ArgumentParser(
        description="Update Public IP to Route53",
        usage='''update_ip.py --zone_name <zone_name> --fqdn <fqdn>''')
    parser.add_argument('--zone_name', '-z', help="Zone Name (i.e. example.com)")
    parser.add_argument('--fqdn', '-f', help="Fully Qualified Domain Name (i.e. home.example.com)")
    parser.add_argument('--cmd-to-retrieve-public-ip', '-c', help="Command to retrieve public ip.", default="dig +short myip.opendns.com @resolver1.opendns.com")
    args = parser.parse_args()
    UpdateIP(args.zone_name, args.fqdn)
