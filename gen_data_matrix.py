#!/usr/bin/env python3

import sys, os, time
from data_matrix import *

def signal_handler(signal, frame):
    sys.exit(0)

def check_right_num_arguments():
    if len(sys.argv) != 3:
        print("Usage:	{} DocumentType Year".format(sys.argv[0]))
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

def check_matrix_exists():
    if not os.path.isfile('data_matrix.csv'):
        with open('data_matrix.csv', 'w') as data_matrix:
            data_matrix.write('PATENT_NO')

def write_to_log_file(DOCTYPE, YEAR, DOC_NO, START, TIME):
    with open('log_file.txt', 'a') as log_file:
        log_file.write(DOCTYPE+"/"+YEAR+"/"+DOC_NO)
        log_file.write(" --- ")
        log_file.write(str((TIME - START)/60))
        log_file.write(" minutes\n")



if __name__=='__main__':
    check_right_num_arguments()
    DOCTYPE=sys.argv[1]
    YEAR=sys.argv[2]
    check_doc_year_path(DOCTYPE, YEAR)
    check_matrix_exists()
    start_time = time.time()

    try:
        while True:
            for doc_number in os.listdir(DOCTYPE+"/"+YEAR):
                if doc_already_in_data_matrix('data_matrix.csv', DOCTYPE+"/"+YEAR+"/"+doc_number):
                    continue
                print("Creating data matrix for {}".format(doc_number))
                add_file_to_data_matrix('data_matrix.csv', DOCTYPE+"/"+YEAR+"/"+doc_number)
                write_to_log_file(DOCTYPE, YEAR, doc_number, start_time, time.time())
                time.sleep(.15)
    except KeyboardInterrupt:
        print("Quitting")
        sys.exit()
