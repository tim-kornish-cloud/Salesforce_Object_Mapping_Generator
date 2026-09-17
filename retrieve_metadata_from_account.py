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

# get username from credentials
username = Cred.get_username(database, environment)
# get password from credentials
password = Cred.get_password(database, environment)
# get login token from credentials
token = Cred.get_token(database, environment)

# create a instance of simple_salesforce to query and perform operations against salesforce with
sf = SF_Utils.login_to_salesForce(username, password, token)

# set list of field metadata to keep
fields_metadata_to_keep = ['name', 'label', 'type', 'length', 'precision', 'unique', 'nillable', 'picklistValues', 'custom', 'calculated']
# set object to grab metadata for
object = "Account"

# retrieve metadata on account and load into pandas dataframe
account_metadata_df = SF_Utils.retrieve_object_metadata(sf, object, fields_metadata_to_keep)

# rename columns to use target as prefix
account_metadata_df.rename(columns = {'name' : 'Target Field API name',
                                      'label' : 'Target Field Lable',
                                      'type' : 'Target Field Type',
                                      'length' : 'Target Field Length',
                                      'precision' : 'Target Field Precision',
                                      'unique' : 'Target Field is Unique',
                                      'nillable' : 'Target Field is nillable',
                                      'picklistValues' : 'Target Field Picklist Values',
                                      'custom' : 'Target Field is custom',
                                      'calculated' : 'Target Field is Calculated'}, inplace = True)

# create list of fields to add to beginning of mapping document
source_fields_to_add = ['Source Object', 'Source Field', 'Source Field Data Type', 'Source Field Description', 'Transformation Logic', 'Map Field', 'Target Object']

# add mapping fields to metadata fields and return new df
account_mapping_df = Utils.add_mapping_fields(account_metadata_df, source_fields_to_add, True)

account_mapping_df['Target Object'] = object

# create list of all dataframes to add to excel file
dfs = [account_mapping_df]
# mapping document file name
file_name = "Mapping_Document.xlsx"
# name of each sheet in mapping document that coordinates to each dataframe in dfs
sheet_names = ['Account']
# output dataframes in excel file
Utils.write_df_to_excel(dfs, file_name, sheet_names)
#print(account_mapping_df.head())
