# folio-data-import-help
Things that are missing from data import.

## Credentials
Set up a file called folio_creds.ini with your FOLIO information. Use folio_creds.ini.example as a starting place. Your baseURL is the address for your FOLIO Okapi which allows API access. It isn't the same as your regular FOLIO web adress and likely has the word 'Okapi' in it. You can find your Okapi address in your FOLIO setting like https://yourfolio/settings/about

The ini currently assumes you will be providing a token which you can get from your FOLIO developer settings. This workaround is easier for people who use the API on a limited basis and who usually log in with SSO. It shouldn't be used if you're doing things in 'production'.

## kickouts.py
Generates a file of discards and a file of errors based on a job ID from data import and the original file you were importing. **You must use the original file because matching is based on the order of the records.** We cannot recreate the file from data import because no MARC exists in FOLIO for MARC records that were not saved. We match on order because title is an even less reliable match point.