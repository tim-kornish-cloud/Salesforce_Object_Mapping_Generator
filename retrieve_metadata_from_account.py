"""
Author: Timothy Kornish
CreatedDate: September - 15 - 2026
Description:
             # log into salesforce
             # call metadata function on account
             # convert return values into pandas dataframe
             # add empty columns for source system to map to target SF Account fields
             # write df to an excel file in a single tab

"""

import numpy as np
import pandas as pd
import os
import json
from custom_db_utilities import  Salesforce_Utilities, Custom_Utilities
from credentials import Credentials

# show all columns in print output
pd.set_option('display.max_columns', None)

# create and instance of the custom salesforce utilities class used to interact with Salesforce
SF_Utils = Salesforce_Utilities()
# create and instance of the custom utilities class used to format and modify dataframe data
Utils = Custom_Utilities()
# create instance of credentials class where creds are stored to load into the script
Cred = Credentials()

# declare which environment this script will perform operations against,
# can have multiple environments in the same script at the same time
environment = 'Dev'

# set database to Salesforce
database = "Salesforce"

# set up directory pathway to load csv data and output fallout and success results to
dir_path = os.path.dirname(os.path.realpath(__file__))

# set up fallout ans success path to save files to
# success file path
success_file = dir_path + "\\Output\\INSERT\\SUCCESS_Insert_" + environment + "_" + database + ".csv"
# fallout file path
fallout_file = dir_path + "\\Output\\INSERT\\FALLOUT_Insert_" + environment + "_" + database + ".csv"


# get username from credentials
username = Cred.get_username(database, environment)
# get password from credentials
password = Cred.get_password(database, environment)
# get login token from credentials
token = Cred.get_token(database, environment)

# create a instance of simple_salesforce to query and perform operations against salesforce with
sf = SF_Utils.login_to_salesForce(username, password, token)

# set list of field metadata to keep
fields_metadata_to_keep = ['label', 'length', 'name', 'type', 'unique', 'nillable', 'picklistValues', 'custom', 'calculated']
# set object to grab metadata for
object = "Account"

account_metadata_df = SF_Utils.retrieve_object_metadata(sf, object, fields_metadata_to_keep)

print(account_metadata_df.head())
# fields_dict = json.loads(json.dumps(sf.Account.describe()['fields']))
#
# fields_df = pd.DataFrame(fields_dict)
#
# mapping_df = fields_df[['label', 'length', 'name', 'type', 'unique', 'nillable', 'picklistValues', 'custom', 'calculated']]
#
# #fields_df.to_csv('account_fields.csv', index=False)
# mapping_df.to_csv('mapping_doc_account_fields.csv', index=False)
