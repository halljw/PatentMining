#!/usr/bin/env python3


import sys, os, csv
from generate_data_matrix import *
from master_matrix import *
from data_matrix_utils import *

"""
Aggregates the data of a given data matrix into master_matrix.csv
Data is stored in output file:
	master_matrix.csv

Use keyboard interrupt to halt aggregation.
"""
def check_num_arguments():
  if len(sys.argv) != 3:
    print("Usage:	{} DocumentType data_matrix)".format(sys.argv[0]))
    print("data_matrix is of format YEAR_BATCHNUM_data_matrix.csv")
    exit()

def check_matrix(YEAR, BATCH_NUM):
  dm = "Data_Matrices/"+str(YEAR)+"_"+str(BATCH_NUM)+"_data_matrix.csv"
  if not os.path.isfile(dm):
    print("{} does not exist".format(dm))
    exit()

def check_master_matrix(matrix):
  if not os.path.isfile('master_matrix.csv'):
    with open('master_matrix.csv', 'w') as mm:
      writer=csv.writer(mm, lineterminator='\n')
      header = ['PATENT_NO'] + matrix.words()
      writer.writerow(header)


def check_log(YEAR, BATCH_NUM):
  lf = "Log_Files/"+str(YEAR)+"_"+str(BATCH_NUM)+"_log_file.txt"
  if not os.path.isfile(lf):
    print("{} does not exist".format(lf))
    exit()

def batch_already_in_master_matrix(master_matrix, batch):
  with open(master_matrix, 'r') as mm:
    reader = csv.reader(mm)
    next(reader)
    m_documents = [line[0] for line in reader]
  if not m_documents:
    return False
  with open('Data_Matrices/'+batch, 'r') as b:
    reader = csv.reader(b)
    documents = [line[0] for line in reader]
  for doc in documents:
    if doc in m_documents:
      return True
  return False

def load_master_matrix():
  matrix = Master_Matrix()
  if os.path.isfile('master_matrix.csv'):
    with open('master_matrix.csv', 'r') as mm:
      reader = csv.reader(mm)
      words = next(reader)[1:]
      for word in words:
        matrix.search(word)
    return matrix
  batches = (batch for batch in sorted(os.listdir("Data_Matrices")))
  for batch in batches:
    with open('Data_Matrices/'+batch, 'r') as batch_file:
      reader = csv.reader(batch_file)
      words = next(reader)[1:]
      for word in words:
        matrix.search(word)
    print(batch, len(matrix.words()))
  check_master_matrix(matrix)
  return matrix


if __name__=="__main__":
  matrix = load_master_matrix()

  batches = (batch for batch in sorted(os.listdir("Data_Matrices")))

  while True:
    print("Processing next batch...")
    try:
      next_batch = next(batches)
      if batch_already_in_master_matrix('master_matrix.csv', next_batch):
        print("Already in master matrix")
        continue

      print('Opening {}...'.format(next_batch))
      with open('Data_Matrices/'+next_batch, 'r') as batch_file:
        reader = csv.reader(batch_file)
        docs = (row for row in reader)
        words = next(docs)[1:]

        while True:
          try:
            next_doc = next(docs)
            next_doc, counts = next_doc[0], next_doc[1:]
            print('\tProcessing {}...'.format(next_doc))
            next_row = []
            next_row.append(next_doc)

            ############
            #Iterature through counts
            for word, count in zip(words,counts):
              index = matrix.search(word)+1
              while index >= len(next_row):
                next_row.append(0)
              next_row[index] = count

            print('\tWriting {} to master matrix...'.format(next_doc))
            with open('master_matrix.csv', 'a') as master_matrix:
              writer = csv.writer(master_matrix, lineterminator='\n')
              writer.writerow(next_row)
          except StopIteration:
            break
      ################
      # Back up master matrix
      ################
      print("Kill process?")
      time.sleep(1)

    except StopIteration:
      print("ALL DOCUMENTS ADDED TO MASTER_MATRIX")
      sys.exit()
    except KeyboardInterrupt:
      print("Quitting")
      sys.exit()

  # Log process in master log file

