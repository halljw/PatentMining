#!/usr/bin/env python3

import csv
from string import punctuation

target_labels = ['TITL', 'ABST', 'DDBK', 'DDSM', 'DDDD', 'CLI', 'CLD']

def add_new_word(data_matrix, new_word):
	"""
	If a new word is found which is not already in the data matrix,
	a column of zeros is added for previous documents
	Takes a data_matrix name, new word string as inputs
	>>> dm_rows = [['PATENT_NO', 'hello', 'world', 'my', 'name', 'is', 'john'], ['012938292', '1', '1', '1', '1', '1', '1'], ['0123456', '3', '4', '1', '1', '5', '1']]
	>>> import csv
	>>> f=open('TEMP.csv', 'w')
	>>> writer=csv.writer(f)
	>>> for row in dm_rows: writer.writerow(row)
	39
	23
	21
	>>> f.close()
	>>> add_new_word('TEMP.csv', 'hi')
	>>> f=open('TEMP.csv', 'r')
	>>> for line in f: print(line,end='')
	PATENT_NO,hello,world,my,name,is,john,hi
	012938292,1,1,1,1,1,1,0
	0123456,3,4,1,1,5,1,0
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
	>>> import csv
	>>> dm_rows = [['PATENT_NO', 'hello', 'world', 'my', 'name', 'is', 'john'], ['012938292', '1', '1', '1', '1', '1', '1'], ['0123456', '3', '4', '1', '1', '5', '1']]
	>>> f=open('TEMP.csv', 'w')
	>>> writer=csv.writer(f)
	>>> for row in dm_rows: writer.writerow(row)
	39
	23
	21
	>>> f.close()
	>>> new_file_text = "ABST:: Is this a dagger I see before me?\nDDHM:: Or art thou but a dagger of the mind?\n"
	>>> f=open('TEMP_NEW_FILE.csv', 'w')
	>>> f.write(new_file_text)
	86
	>>> f.close()
	>>> add_file_to_data_matrix('TEMP.csv', 'TEMP_NEW_FILE.csv')
	>>> f=open('TEMP.csv', 'r')
	>>> for line in f: print(line,end='')
	PATENT_NO,hello,world,my,name,is,john,this,a,dagger,i,see,before,me
	012938292,1,1,1,1,1,1,0,0,0,0,0,0,0
	0123456,3,4,1,1,5,1,0,0,0,0,0,0,0
	TEMP_NEW_FILE.csv,0,0,0,0,1,0,1,1,1,1,1,1,1
	>>> f=open('TEMP_EMPTY_MATRIX.csv', 'w')
	>>> f.write('PATENT_NO')
	9
	>>> f.close()
	>>> add_file_to_data_matrix('TEMP_EMPTY_MATRIX.csv', 'TEMP_NEW_FILE.csv')
	>>> f=open('TEMP_EMPTY_MATRIX.csv', 'r')
	>>> for line in f: print(line,end='')
	PATENT_NO,is,this,a,dagger,i,see,before,me
	TEMP_NEW_FILE.csv,1,1,1,1,1,1,1,1
	"""
	# Generate list of words already in data matrix
	# Store words in list dm_words
	# Store	words with 0 count in dictionary word_dict
	with open(data_matrix, 'r') as old_data_matrix:
		reader = csv.reader(old_data_matrix)
		for line in reader:
			dm_words=line[1:]
			break
	word_dict = {word: 0 for word in dm_words}

	# Open input file, split at "::" to check heading; if in appropriate heading, words counted
	# Words stripped of punctuation, split on whitespace
	# Words counted and stored in dictionary word_dict
	with open(new_file, 'r') as f:
		for line in f:
			try:
				words = ''.join([char for char in line.split("::")[1].lower().strip() if not char in punctuation]).split()
				for word in words:
					if word.isalpha():
						if word in word_dict:
							word_dict[word] += 1
						else:
							dm_words.append(word)
							word_dict[word] = 1
							add_new_word(data_matrix, word)
			except:
				pass
	# Generate list of values in order of words in original data_matrix
	values = [str(word_dict[word]) for word in dm_words]
	new_row = [new_file] + values

	# Append new row of values to data_matrix
	with open(data_matrix, 'a') as new_data_matrix:
		writer = csv.writer(new_data_matrix, lineterminator='\n')
		writer.writerow(new_row)

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
	

if __name__=='__main__':
	import doctest
	doctest.testmod()
