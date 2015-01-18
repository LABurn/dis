#!/usr/bin/env python

import urllib
import sqlite3

disease_list_file = open("diseases.txt") # File containing list of diseases, one per line in the form "disease,year-cured"

# Connect to SQLite3 database
connection = sqlite3.connect("diseasedata.db")
cursor = connection.cursor()
table_name = "publicationdata"

# Loop through lines in file
for line in disease_list_file:

	# Parse out disease name and year cured
	term = line.split(",")[0]
	cured_year = int(line.split(",")[1])

	# Check if disease is already in the database
	cursor.execute("SELECT * FROM " + table_name + " WHERE disease='" + term + "'")
	if cursor.fetchone() is None:

		# Loop to query publications up to 20 years before cure found
		for year in range(cured_year - 20, cured_year):

			# Enter query for single year into URL
			query_url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=" + term + "&datetype=pdat&mindate=" + str(year) + "&maxdate=" + str(year)
			query_xml = urllib.urlopen(query_url).read()

			# Parse out publication count for that year
			count = query_xml.split("<Count>")[1].split("</Count>")[0]

			# Add info as a row in sqlite table
			cursor.execute("INSERT INTO " + table_name + " VALUES ('" + term + "'," + str(year - cured_year) + "," + str(count) + ")")
			print term + " " + str(year) + ", " + str(count) + " publications"
			if count == 0:
				print "^ Warning, no publications for above year"

# Close up and finish
connection.commit()
connection.close()
print "Done."
exit()
