import csv
import os
import datetime
from openaigen import *

def iterate_docs(promptNum):
    directory = "./documents"
    currenttime = datetime.datetime.now()

    program_run = ["program run time", currenttime]
    
    with open('results/results.csv', 'a', newline='') as file:
        writetocsv = csv.writer(file)
        writetocsv.writerow(program_run)

    for filename in os.scandir(directory):
        doc = filename
        filepath = directory + "/" + doc.name
        utterances = send_prompt_with_document(filepath, promptNum)
        postprocess(utterances)

def postprocess(list):
    file_path = 'results/results.csv'
    with open(file_path, 'a', newline='') as file:
        writetocsv = csv.writer(file)
        writetocsv.writerow(list)

iterate_docs(2)
