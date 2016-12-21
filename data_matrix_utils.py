#!/usr/bin/env python3

import csv, os
from string import punctuation
from trie import *

"""
Methods used in generating data matrices from patent text documents.
Includes methods for ensuring matrices are being generated correctly.
"""
def add_new_word(data_matrix, new_word):
	r"""
	If a new word is found which is not already in the data matrix,
	a column of zeros is added for previous documents
	Takes a data_matrix name, new word string as inputs
	>>> dm_rows = [['PATENT_NO', 'hello', 'world', 'my', 'name', 'is', 'john'], ['012938292', '1', '1', '1', '1', '1', '1'], ['0123456', '3', '4', '1', '1', '5', '1']]
	>>> import csv
	>>> f=open('TEMP.csv', 'w')
	>>> writer=csv.writer(f, lineterminator='\n')
	>>> for row in dm_rows: writer.writerow(row)
	38
	22
	20
	>>> f.close()
	>>> add_new_word('TEMP.csv', 'hi')
	>>> f=open('TEMP.csv', 'r')
	>>> for line in f: print(line,end='')
	PATENT_NO,hello,world,my,name,is,john,hi
	012938292,1,1,1,1,1,1,0
	0123456,3,4,1,1,5,1,0
	>>> os.remove('TEMP.csv')
	"""

	# Read old data_matrix into dm_rows
	with open(data_matrix, 'r') as old_data_matrix:
		reader = csv.reader(old_data_matrix)
		dm_rows = [row for row in reader]

	# Append new word to dm_rows
	# Append zero as value for the new word to all previous documents
	dm_rows[0].append(new_word)
	for row in dm_rows[1:]:
		row.append('0')


	# Rewrite results to original data_matrix file
	with open(data_matrix, 'w') as new_data_matrix:
		writer = csv.writer(new_data_matrix, lineterminator='\n')
		for row in dm_rows:
			writer.writerow(row)


def add_file_to_data_matrix(data_matrix, new_file):
	r"""
	Returns the number of words added contributed to the data matrix
	by the present file
	>>> import csv
	>>> dm_rows = [['PATENT_NO', 'hello', 'world', 'my', 'name', 'is', 'john'], ['012938292', '1', '1', '1', '1', '1', '1'], ['0123456', '3', '4', '1', '1', '5', '1']]
	>>> f=open('TEMP.csv', 'w')
	>>> writer=csv.writer(f, lineterminator='\n')
	>>> for row in dm_rows: writer.writerow(row)
	38
	22
	20
	>>> f.close()
	>>> new_file_text = "ABST:: Is this a dagger I see before me?\nDDHM:: Or art thou but a dagger of the mind?\n"
	>>> f=open('TEMP_NEW_FILE.csv', 'w')
	>>> f.write(new_file_text)
	86
	>>> f.close()
	>>> add_file_to_data_matrix('TEMP.csv', 'TEMP_NEW_FILE.csv')
	14
	>>> f=open('TEMP.csv', 'r')
	>>> for line in f: print(line,end='')
	PATENT_NO,hello,world,my,name,is,john,this,a,dagger,i,see,before,me,or,art,thou,but,of,the,mind
	012938292,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0
	0123456,3,4,1,1,5,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0
	TEMP_NEW_FILE.csv,0,0,0,0,1,0,1,2,2,1,1,1,1,1,1,1,1,1,1,1
	>>> f=open('TEMP_EMPTY_MATRIX.csv', 'w')
	>>> f.write('PATENT_NO')
	9
	>>> f.close()
	>>> add_file_to_data_matrix('TEMP_EMPTY_MATRIX.csv', 'TEMP_NEW_FILE.csv')
	15
	>>> f=open('TEMP_EMPTY_MATRIX.csv', 'r')
	>>> for line in f: print(line,end='')
	PATENT_NO,is,this,a,dagger,i,see,before,me,or,art,thou,but,of,the,mind
	TEMP_NEW_FILE.csv,1,1,2,2,1,1,1,1,1,1,1,1,1,1,1
	>>> os.remove('TEMP_EMPTY_MATRIX.csv')
	>>> os.remove('TEMP.csv')
	>>> os.remove('TEMP_NEW_FILE.csv')
	"""
	# Generate list of words already in data matrix
	# Store words in list dm_words
	# Store	words with 0 count in dictionary word_dict
	with open(data_matrix, 'r') as old_data_matrix:
		reader = csv.reader(old_data_matrix)
		for line in reader:
			dm_words=line[1:]
			break
	
	trie = Trie()
	for word in dm_words:
		trie.insert(word)

	# Open input file, split at "::" to remove heading
	# Words stripped of punctuation, split on whitespace
	# Words counted and stored in dictionary word_dict
	new_words_added = 0
	with open(new_file, 'r') as f:
		for line in f:
			new_words = trie.count_line(line)
			for new_word in new_words:
				add_new_word(data_matrix, new_word)
				new_words_added += 1
			dm_words += new_words


	# Generate list of values in order of words in original data_matrix
	values = [str(trie.get_val(word)) for word in dm_words]
	new_row = [new_file] + values

	# Append new row of values to data_matrix
	with open(data_matrix, 'a') as new_data_matrix:
		writer = csv.writer(new_data_matrix, lineterminator='\n')
		writer.writerow(new_row)

	return new_words_added

def doc_already_in_data_matrix(data_matrix, new_file):
	"""
	If target file is already recorded in data_matrix,
	return True; return False otherwise
	"""
	with open(data_matrix, 'r') as old_data_matrix:
		reader = csv.reader(old_data_matrix)
		documents = [line[0] for line in reader]
	if new_file in documents: return True
	return False

def check_up(year, batch_number):
	"""
	Make sure data_matrix is being constructed correctly.
		A) The Log File and the Data Matrix should be of the same length
		B) Each Document Number in the Log File should be present in Data Matrix
		C) All words in Data Matrix header should be alphabetic only
		D) Number of words added recording in Log File should match the number
		   of columns in the Data Matrix header
	"""
	dm_name = "Data_Matrices/"+str(year) + "_" + str(batch_number) + "_data_matrix.csv"
	lf_name = "Log_Files/"+str(year) + "_" + str(batch_number) + "_log_file.txt"

	dm_lines = sum(1 for line in open(dm_name,'r'))
	lf_lines = sum(1 for line in open(lf_name,'r'))
	if dm_lines != lf_lines:
		raise ValueError("DATA MATRIX {}_{} HAS DIFFERENT NUMBER OF LINES THAN LOG FILE".format(year, batch_number))

	with open(dm_name,'r') as dm:
		with open(lf_name, 'r') as lf:
			dm_reader = csv.reader(dm)
			dm_numbers = [line[0] for line in dm_reader]
			lf_numbers = [line.split()[0] for line in lf]
	if dm_numbers != lf_numbers:
		print(dm_numbers)
		print(lf_numbers)
		raise ValueError("DATA MATRIX {}_{} CONTAINS DIFFERENT DOCUMENTS THAN LOG FILE".format(year, batch_number))

	with open(dm_name,'r') as dm:
		dm_reader = csv.reader(dm)
		for line in dm_reader:
			words = line[1:]
			break
	for word in words:
		if not word.isalpha():
			raise ValueError("DATA MATRIX {}_{} CONTAINS NON-ALPHABETIC WORD".format(year, batch_number))

	with open(lf_name,'r') as lf:
		line = next(lf)
		lf_words = sum([float(line.split(" --- ")[2].split()[0]) for line in lf])
	if len(words) != lf_words:
		raise ValueError("DATA MATRIX {}_{} AND LOG FILE COUNT DIFFERENT NUMBER OF WORDS".format(year, batch_number))

if __name__=='__main__':
	import doctest
	doctest.testmod()
