#!/usr/bin/python

import boto3
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
            if os.path.isfile(output_file):
                os.remove(output_file)
            with open(output_file,"a") as json_file:
                for i, policy in enumerate(file_content["Statement"]):
                    if "Resource" in policy:
                        if type(file_content["Statement"][i]["Resource"]) == list:
                            for j,resource in enumerate(policy["Resource"]):
                               if "REGION_HERE" in policy["Resource"][j]:
                                  file_content["Statement"][i]["Resource"][j] = file_content["Statement"][i]["Resource"][j].replace("REGION_HERE",args.region)
                                  if "COMPONENT_NAME_HERE" in policy["Resource"][j]:
                                   file_content["Statement"][i]["Resource"][j] = file_content["Statement"][i]["Resource"][j].replace("COMPONENT_NAME_HERE",args.component)           
                        elif "REGION_HERE" in policy["Resource"]:
                            file_content["Statement"][i]["Resource"] = file_content["Statement"][i]["Resource"].replace("REGION_HERE",args.region)

                        elif "COMPONENT_NAME_HERE" in policy["Resource"]:
                            file_content["Statement"][i]["Resource"] = file_content["Statement"][i]["Resource"].replace("COMPONENT_NAME_HERE",args.component)

                json.dump(file_content, json_file,indent=4, sort_keys=True)
            print "file has been updated"
        else:
            print "Policy does not exists"




if __name__ == '__main__':

  args = parse_arguments()

  my_services = args.services.split(",")

  print args.region
  print args.component
  merge_json(my_services)
