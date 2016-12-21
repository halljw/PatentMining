#!/usr/bin/env python3

import sys, os, time
from shutil import copyfile
from subprocess import call
from data_matrix_utils import *
from trie import *

"""
Constructs data matrices from patent document text files of the format:

	PATENT_NO,word,word,word...
	TYPE/YEAR/NUMBER,count,count,count...
	TYPE/YEAR/NUMBER,count,count,count...
	...

Documents are processed in batches of 100 for convenience. Use keyboard interrupt to
  halt processing. Back up files are written to present directory every ten documents to
  ensure halting progress does not result in significant loss of data.

Specify document type (patent or application) and year to begin data matrix construction.
  If data matrix for a given document already exists, given document is skipped. To skip
  checking for documents which already exist, specify the latest batch number which has
  already been processed (specify multiple of 100).

Assumes presence of directory structure:

	Current Directory
	   Data_Matrices
	   Log_Files
	   Pat
	      2005
	      2006
	      ...
	   App
	      2005
	      2006
	      ...

Log files contain list of document numbers added for each batch of 100 documents, as well
  as the time to write a document and the number of original words contributed by each
  document.
"""
def check_right_num_arguments():
    if len(sys.argv) == 4:
        if int(sys.argv[3])%100 != 0:
            print("Usage:	{} DocumentType Year (Batch_Number)".format(sys.argv[0]))
            print("	DocumentType is 'App' or 'Pat'")
            print("	Year is four digits")
            exit()
    elif len(sys.argv) != 3:
            print("Usage:	{} DocumentType Year (Batch_Number)".format(sys.argv[0]))
            print("	DocumentType is 'App' or 'Pat'")
            print("	Year is four digits")
            exit()

def check_doc_year_path(DOCTYPE, YEAR):
    if not os.path.isdir(DOCTYPE):
        print("Usage:	{} directory doesn't exist".format(DOCTYPE))
        exit()
    if not os.path.isdir(DOCTYPE+"/"+YEAR):
        print("Usage:	{} directory doesn't exist".format(DOCTYPE+"/"+YEAR))
        exit()

def check_matrix_exists(YEAR, batch_number):
    dm = "Data_Matrices/" + str(YEAR) + "_" + str(batch_number) + "_data_matrix.csv"
    if not os.path.isfile(dm):
        with open(dm, 'w') as data_matrix:
            data_matrix.write('PATENT_NO')

def check_log_exists(YEAR, batch_number):
    lf = "Log_Files/" + str(YEAR) + "_" + str(batch_number) + "_log_file.txt"
    if not os.path.isfile(lf):
        with open(lf, 'w') as log_file:
            log_file.write('PATENT_NO\t\tTIME TO WRITE\t\tWORDS ADDED BY FILE\n')
        return 0
    else:
        with open(lf, 'r') as log_file:
            lines = log_file.readlines()
        return float(lines[-1].split()[2])*60

def write_to_log_file(DOCTYPE, YEAR, batch_num, DOC_NO, START, TIME, LAST, NEW_WORDS):
    lf = "Log_Files/" + str(YEAR) + "_" + str(batch_num) + "_log_file.txt"
    with open(lf, 'a') as log_file:
        log_file.write(DOCTYPE+"/"+YEAR+"/"+DOC_NO)
        log_file.write(" --- ")
        log_file.write(str((LAST + TIME - START)/60))
        log_file.write(" minutes")
        log_file.write(" --- ")
        log_file.write(str(NEW_WORDS)+" new words added\n")

def write_back_ups(YEAR, batch_number):
    dm = "Data_Matrices/" + str(YEAR) + "_" + str(batch_number) + "_data_matrix.csv"
    lf = "Log_Files/" + str(YEAR) + "_" + str(batch_number) + "_log_file.txt"
    copyfile(dm, 'backup_data_matrix.csv')
    copyfile(lf, 'backup_log_file.txt')


if __name__=='__main__':
    check_right_num_arguments()
    DOCTYPE=sys.argv[1]
    YEAR=sys.argv[2]
    check_doc_year_path(DOCTYPE, YEAR)
    start_time = time.time()
    try:
        batch_number = int(sys.argv[3])
    except:
        batch_number = 100

    docs = (doc for doc in sorted(os.listdir(DOCTYPE+"/"+YEAR)))
    dm_name = "Data_Matrices/" + str(YEAR) + "_" + str(batch_number) + "_data_matrix.csv"
    lf_name = "Log_Files/" + str(YEAR) + "_" + str(batch_number) + "_log_file.txt"

    for i in range(batch_number - 100):
        next(docs)

    while True:
        try:
            for i in range(100):
                check_matrix_exists(YEAR, batch_number)
                last_end_time = check_log_exists(YEAR, batch_number)

                next_doc = next(docs)

                if doc_already_in_data_matrix(dm_name, DOCTYPE+"/"+YEAR+"/"+next_doc):
                    continue

                check_up(YEAR, batch_number)
                print("Creating data matrix for {} in batch {}".format(next_doc, batch_number))
                new_words=add_file_to_data_matrix(dm_name, DOCTYPE+"/"+YEAR+"/"+next_doc)
                write_to_log_file(DOCTYPE, YEAR, batch_number, next_doc, start_time, time.time(), last_end_time, new_words)
                if i%10 == 0:
                    print("Kill process?")
                    time.sleep(1)
                if i%10 == 5:
                    write_back_ups(YEAR, batch_number)
            batch_number += 100

            # PUSH DATA MATRICES AND LOGS TO GIT FOR SAFE KEEPING
            os.system("git add Data_Matrices")
            os.system("git add Log_Files")
            os.system("git commit -m 'Updated matrices and logs'")
            os.system("git push origin master")

            dm_name = "Data_Matrices/" + str(YEAR) + "_" + str(batch_number) + "_data_matrix.csv"
            lf_name = "Log_Files/" + str(YEAR) + "_" + str(batch_number) + "_log_file.txt"


        except StopIteration:
            print("ALL DOCUMENTS IN "+DOCTYPE+"/"+YEAR+" PARSED")
            break
        except KeyboardInterrupt:
            print("Quitting")
            sys.exit()
