#!/usr/bin/env python

import urllib
import sqlite3

disease_list_file = open("diseases.txt") # File containing list of diseases, one per line in the form "disease,year-cured"

# Connect to SQLite3 database
connection = sqlite3.connect("diseasedata.db")
cursor = connection.cursor()

# Loop through lines in file
for line in disease_list_file:

	# Parse out disease name and year cured
	term = line.split(",")[0]
	cured_year = int(line.split(",")[1])

	# Loop to query publications up to 20 years before cure found
	for year in range(cured_year - 19, cured_year + 1):

		# Enter query for single year into URL
		query_url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pmc&term=" + term + "&datetype=pdat&mindate=" + str(year) + "&maxdate=" + str(year)
		query_xml = urllib.urlopen(query_url).read()

		# Parse out publication count for that year
		count = query_xml.split("<Count>")[1].split("</Count>")[0]

		# Add info as a row in sqlite table
		cursor.execute("INSERT INTO publicationdata VALUES ('" + term + "'," + str(year) + "," + str(count) + ")")
		print term + " " + str(year) + ", " + str(count) + " publications"

# Close up and finish
connection.commit()
connection.close()
print "Done."
exit()
