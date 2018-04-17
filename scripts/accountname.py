#!/usr/bin/python
import boto3
import argparse
from pprint import pprint
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import tzinfo, timedelta
import yaml
import subprocess
import json
import sys

CLOUD_SOR_AURORA_URL='sorbilling.deere.com'
CLOUD_SOR_AURORA_USER='AQECAHhT/jMDhQDpgiB6MOMo41eYkLiejy6FjE9vthNHhkKtkAAAAGcwZQYJKoZIhvcNAQcGoFgwVgIBADBRBgkqhkiG9w0BBwEwHgYJYIZIAWUDBAEuMBEEDJAtAfyA/nT9FY1tWAIBEIAkOOTkMWj4OTlMrPsPhSW2oj5LDJFgNG210RwXQRktEKvKu9X7'
CLOUD_SOR_AURORA_PASSWORD='AQECAHhT/jMDhQDpgiB6MOMo41eYkLiejy6FjE9vthNHhkKtkAAAAGwwagYJKoZIhvcNAQcGoF0wWwIBADBWBgkqhkiG9w0BBwEwHgYJYIZIAWUDBAEuMBEEDAPUc3b1UXvap2YJwAIBEIAp+XiYmqN6W7C+mFEWHSlKB5BWaE92FRoIhd02cYHQ4bqBqbJJ3xSiNgk='
CLOUD_SOR_AURORA_DB_NAME='clouddb'

if __name__ == '__main__':

  #args = parse_arguments()

  curlReponse=subprocess.check_output(["curl", "-k", "-X", "GET", "-H", "Accept: application/json", "https://sorapi.deere.com/unprotected/accounts"])
  my_accounts = json.loads(curlReponse)

  my_excluded_accounts = []
  my_bind_cis = []

  for my_account in my_accounts["accounts"]:
    if str(my_account["accountEndTs"]).strip() != "None":
      continue

    my_break = False
    for my_excluded_account in my_excluded_accounts:
      #print '(' + my_excluded_account + ') (' + str(my_account["aliasName"]).strip() + ')'
      if (str(my_account["aliasName"]).strip() == my_excluded_account):
        my_break = True
        continue

    if(my_break):
      continue

    my_account_number = str(my_account["awsAccountNumber"]).strip()
    print my_account_number
