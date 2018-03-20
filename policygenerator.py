#!/usr/bin/python
# import boto3
import argparse
import json
import os
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


def merge_json(input_files,output_file="output.json"):
    # read json file from current dir
    for file in input_files:
        file = file + ".json"
        if os.path.isfile(file):
            # Read file content
            with open(file,"r") as f:
                file_content = json.load(f)
            # Write file content
            with open(output_file,"a") as json_file:
                json.dump(file_content, json_file,indent=4, sort_keys=True)
            print "file has been updated"
        else:
            print "Policy does not exists"

                # Update Region
                # if "Resource" in file_content:
                #    print file_content



if __name__ == '__main__':

  args = parse_arguments()

  my_services = args.services.split(",")

  print args.region
  print args.component
  merge_json(my_services)