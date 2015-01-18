#!/usr/bin/env python

import urllib
import sqlite3
import numpy as np

def populateDatabase(disease_list_file, database_file, table_name):
	"""Populates the local database file with information queried from the NCBI Entrez
	utilities for the 20 years leading up to the disease's cure.
	All parameters are strings, disease_list_file should referece a text file containing
	diseases and the year they were cured in the form 'disease,year' one per line,
	database_file should referece an SQLite3 database file, table_name should reference
	the name of a table within the database with columns for disease name, year queried,
	and publication count."""
	connection = sqlite3.connect(database_file)
	cursor = connection.cursor()
	# Iterate through list file
	for line in disease_list_file:
		term = line.split(",")[0]
		cured_year = int(line.split(",")[1])
		cursor.execute("SELECT * FROM " + table_name + " WHERE disease='" + term + "'")
		# Check if disease is already in database
		if cursor.fetchone() is None:
			for year in range(cured_year - 20, cured_year):
				query_url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=" + term + "&datetype=pdat&mindate=" + str(year) + "&maxdate=" + str(year)
				query_xml = urllib.urlopen(query_url).read()
				count = query_xml.split("<Count>")[1].split("</Count>")[0]
				cursor.execute("INSERT INTO " + table_name + " VALUES ('" + term + "'," + str(year - cured_year) + "," + str(count) + ")")
				print(term + " " + str(year) + ", " + str(count) + " publications")
				# Warn if publication count is unsatisfactory
				if count == 0:
					print("^ Warning, no publications for the above year")
	# Close up and finish
	connection.commit()
	connection.close()
	return

def getDataArrays(database_file, table_name):
	"""Returns 3 arrays containing the tuples of data for lower, middle, and upper
	portions of the data set. The tuples are organized by year, eacch year having
	a count of publications for that year."""
	connection = sqlite3.connect(database_file)
	cursor = connection.cursor()
	cursor.execute("SELECT disease, SUM(publications) FROM " + table_name + " GROUP BY disease")
	result = cursor.fetchall()
	pubs, lower_block, middle_block, upper_block = [], [], [], []
	# Find total number of publications we are working with and separate into 3 blocks
	for i in range(0, len(result)):
		pubs.append(int(result[i][1]))
	array = np.array(pubs)
	for j in range(0, len(result)):
		cursor.execute("SELECT year, publications FROM " + table_name + " WHERE disease='" + str(result[j][0]) + "' ORDER BY year ASC")
		info = cursor.fetchall()
		if int(result[j][1]) <= int(np.percentile(array, 33)):
			lower_block.append(info)
		elif int(result[j][1]) <= int(np.percentile(array, 66)):
			middle_block.append(info)
		else:
			upper_block.append(info)
	return lower_block, middle_block, upper_block

if __name__ == "__main__":
	a, b, c = getDataArrays("diseasedata.db", "publicationdata")
	print(a)
	print(b)
	print(c)
