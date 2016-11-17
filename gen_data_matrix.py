#!/usr/bin/env python3


################################
"""
FUTURE JOHN, SET THIS UP TO WORK ON BATCHES OF A HUNDRED
THIS WILL SAVE YOU HEARTACHE IN THE FUTURE
BUT REQUIRES A REWRITE OF HOW YOU DID STUFF BELOW, EACH ONE NEEDS THE BATCH NUMBER
IN THE FILE NAME FROM THE START. DO IT
"""


import sys, os, time
from shutil import copyfile
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

def check_matrix_exists(YEAR, batch_number):
    dm = str(YEAR) + "_" + str(batch_number) + "_data_matrix.csv"
    if not os.path.isfile(dm):
        with open(dm, 'w') as data_matrix:
            data_matrix.write('PATENT_NO')

def check_log_exists(YEAR, batch_number):
    lf = str(YEAR) + "_" + str(batch_number) + "_log_file.txt"
    if not os.path.isfile(lf):
        with open(lf, 'w') as log_file:
            log_file.write('PATENT_NO\t\tTIME TO WRITE\t\tWORDS ADDED BY FILE\n')
        return 0
    else:
        with open(lf, 'r') as log_file:
            lines = log_file.readlines()
        return float(lines[-1].split()[2])*60

def write_to_log_file(DOCTYPE, YEAR, batch_num, DOC_NO, START, TIME, LAST, NEW_WORDS):
    lf = str(YEAR) + "_" + str(batch_num) + "_log_file.txt"
    with open(lf, 'a') as log_file:
        log_file.write(DOCTYPE+"/"+YEAR+"/"+DOC_NO)
        log_file.write(" --- ")
        log_file.write(str((LAST + TIME - START)/60))
        log_file.write(" minutes")
        log_file.write(" --- ")
        log_file.write(str(NEW_WORDS)+" new words added\n")

def write_back_ups(YEAR, batch_number):
    dm = str(YEAR) + "_" + str(batch_number) + "_data_matrix.csv"
    lf = str(YEAR) + "_" + str(batch_number) + "_log_file.txt"
    copyfile(dm, 'backup_data_matrix.csv')
    copyfile(lf, 'backup_log_file.txt')

def batch(year, batch_number):
    copyfile('data_matrix.csv', str(YEAR)+'_'+str(batch_number)+'_data_matrix.csv')
    copyfile('log_file.txt', str(YEAR)+'_'+str(batch_number)+'_log_file.txt')

if __name__=='__main__':
    check_right_num_arguments()
    DOCTYPE=sys.argv[1]
    YEAR=sys.argv[2]
    check_doc_year_path(DOCTYPE, YEAR)
    start_time = time.time()

    docs = (doc for doc in sorted(os.listdir(DOCTYPE+"/"+YEAR)))
    batch_number = 100
    dm_name=str(YEAR)+"_"+str(batch_number)+"_data_matrix.csv"
    lf_name=str(YEAR)+"_"+str(batch_number)+"_log_file.txt"

    while True:
        try:
            for i in range(100):
                check_matrix_exists(YEAR, batch_number)
                last_end_time = check_log_exists(YEAR, batch_number)
                check_up(YEAR, batch_number)

                next_doc = next(docs)

                if doc_already_in_data_matrix(dm_name, DOCTYPE+"/"+YEAR+"/"+next_doc):
                    continue
                print("Creating data matrix for {} in batch {}".format(next_doc, batch_number))
                new_words=add_file_to_data_matrix(dm_name, DOCTYPE+"/"+YEAR+"/"+next_doc)
                write_to_log_file(DOCTYPE, YEAR, batch_number, next_doc, start_time, time.time(), last_end_time, new_words)
                if i%10 == 0:
                    print("Kill process?")
                    time.sleep(1)
                if i%10 == 5:
                    write_back_ups(YEAR, batch_number)
            batch_number += 100

        except StopIteration:
            print("ALL DOCUMENTS IN "+DOCTYPE+"/"+YEAR+" parsed")
            break
        except KeyboardInterrupt:
            print("Quitting")
            sys.exit()
