# folio-data-import-help
Things that are missing from data import.

## kickouts.py
Generates a file of discards and a file of errors based on a job ID from data import and the original file you were importing. **You must use the original file because matching is based on the order of the records.** We cannot recreate the file from data import because no MARC exists in FOLIO for MARC records that were not saved. We match on order because title is an even less reliable match point.