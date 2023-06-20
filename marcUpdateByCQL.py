#!/usr/bin/env python



import requests
import configparser
from pymarc import MARCReader, Record, Field


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

#available fields
#035 will search by OCLC number or instance identifier
#899 will search by identifier
#020 will search by ISBN





# the records you want to match
marcSourceFile = "/Users/jrc88/folio-data-import-help/data/BNA_NEW_RECORDS_test1.mrc"
with open("data/BNA_NEW_RECORDS_test1_matchedRecords.mrc", 'wb') as matchedFile, open("data/BNA_NEW_RECORDS_test1_unmatchedRecords.mrc", 'wb') as discardFile :
	with open(marcSourceFile, 'rb') as marcfile:
			marc_reader= MARCReader(marcfile)
			for record in marc_reader:
				queryChunks = []
				#get the fields that contain your match points then arrange them into query strings
				marc035 = record.get_fields('035')
				for f in marc035:
					sf = f.get_subfields('a')
					for a in sf:
						if 'OCoLC' in a:
							queryChunks.append('oclc="' + a +'"')
						else:
							queryChunks.append('identifiers.value="' + a +'"')
				marc899 = record.get_fields('899')
				for f in marc899:
					sf = f.get_subfields('a')
					for a in sf:
						queryChunks.append('(identifiers.value="' + a +'")')

				query = ""
				for i in range(0,len(queryChunks)):
					query = query + queryChunks[i]
					if i < len(queryChunks)-1:
						query = query + " and "

				print('query: ' + query)

				#send the queries to folio then write a matched and unmatched file

				recordSearch = requests.get(baseURL + '/search/instances?limit=100&expandAll=true&query=(' + query + ')',headers=headers).json()
				if recordSearch['totalRecords'] == 1: 
					record.add_ordered_field(
							Field(
								tag = '997',
								indicators = [' ',' '],
								subfields = ['a', recordSearch['instances'][0]['hrid']]
							))
					matchedFile.write(record.as_marc())
				else:
					discardFile.write(record.as_marc())
			
			

