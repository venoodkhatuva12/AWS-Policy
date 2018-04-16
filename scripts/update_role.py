import argparse
import json
import os
import stopwords
from pprint import pprint

def parse_arguments():
  parser = argparse.ArgumentParser()
  parser.add_argument("-a", "--ad_group", help="ad_group",
                    action="store"),
  parser.add_argument("-c", "--child_account_number", help="child_account_number",
                      action="store"),
         args = parser.parse_args()

def json_file(input_files,output_file="output.json"):
    # removing old output file
    if os.path.isfile(output_file):
         os.remove(output_file)

    for file in input_files:
        file = file + ".json"
        if os.path.isfile(file):
            with open(file,"r") as f:
                file_content = json.load(f)
            for i, role in enumerate(file_content["Statement"]):
                if "Sid" in role:
                    role["Sid"] = "Sid" + str(role_number)
                if "Resource" in role:
                    if type(role["Resource"]) == list:
                        for j,resource in enumerate(role["Resource"]):
                           if "ACCOUNT_NUMBER_HERE" in role["Resource"][j]:
                              role["Resource"][j] = role["Resource"][j].replace("ACCOUNT_NUMBER_HERE",args.child_account_number)
                           if "AD_GROUP" in role["Resource"][j]:
                              role["Resource"][j] = role["Resource"][j].replace("AD_GROUP",args.ad_group)
                 output["Statement"].append(role)
                role_number += 1
            
            else:
                print "Role does not exists"
    print output
    # Write file content
    with open(output_file,"a") as json_file:
      json.dump(output, json_file,indent=4, sort_keys=True)
      print "file has been updated"