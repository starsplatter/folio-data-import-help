#!/usr/bin/env python



import requests
import configparser
from pymarc import MARCReader


#set up folio_creds.ini with your information. use the example file as a starting place.
config = configparser.ConfigParser()
config.read('folio_creds.ini')
okapi_tenant = config.get('okapi', 'tenant')
okapi_token = config.get('okapi', 'token')
baseURL = config.get('okapi', 'baseURL')

headers = {
    'x-okapi-tenant': okapi_tenant,
    'x-okapi-token': okapi_token,
    'Accept': "*/*",
    'Accept-Encoding': "gzip, deflate",
    'Connection': "keep-alive",
    'Content-type': "application/json"
    }

# replace with the job summary id from data import
jobSummary = "c2e95ace-0417-4da0-a721-8deb9ede478a"

# replace with marc file you were trying to load, can be anywhere on your computer if
# you enter the path correctly. your output files will be in the data directory
marcSourceFile = "data/aae_complete_processed.mrc"


getJobExecution= requests.get(baseURL + '/metadata-provider/jobLogEntries/' + jobSummary
							   + '?limit=100000', headers=headers).json()

with open(marcSourceFile, 'rb') as marcfile:
		records = []
		marc_reader= MARCReader(marcfile)
		for marc in marc_reader:
			records.append(marc)

with open("data/"+jobSummary + "_errors.mrc", 'wb') as errorFile, open("data/"+jobSummary + "_discards.mrc", 'wb') as discardFile :
	for entry in getJobExecution['entries']:
		actionStatus = 'No Action'
		recordNumber = int(entry['sourceRecordOrder'])
		if 'instanceActionStatus' in entry:
			actionStatus = entry['instanceActionStatus']
		if actionStatus not in ['UPDATED','CREATED','MULTIPLE']: 
			print(entry['sourceRecordTitle'],actionStatus)
			if 'error' in entry:
				errorFile.write(records[recordNumber].as_marc())
			else:
				discardFile.write(records[recordNumber].as_marc())