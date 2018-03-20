#!/usr/bin/python
import boto3
import argparse
import json
from pprint import pprint

def parse_arguments():
  parser = argparse.ArgumentParser()
  parser.add_argument("-r", "--region", help="region",
                      action="store",
                      default="us-east-1")
  parser.add_argument("-c", "--component", help="component",
                      action="store",
                      default="component")
  parser.add_argument("-s", "--services", help="services",
                      action="store",
                      default="services")
  return parser.parse_args()

if __name__ == '__main__':

  args = parse_arguments()

  my_services = args.services.split(",")

  print args.region
  print args.component

  my_big_var = []
  for my_service in my_services:
      my_content = json.load(open(my_service))
      my_big_var.append(my_content)



  pprint(my_big_var)

  print my_service

  my_content = json.load(open(my_service))
  print(my_content)

  if("Resource" in my_content):
     for my_resource in my_content["Resource"]:
       if("REGION_HERE" in my_resource):
         my_resource.replace("REGION_HERE", args.region)

  print(my_content)
