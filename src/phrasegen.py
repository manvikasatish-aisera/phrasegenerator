import csv
import os
import datetime
from openaigen import *

def iterate_docs(promptNum):
    directory = "./documents"
    currenttime = datetime.datetime.now()

    program_run = ["program run time", currenttime]
    result_list = []
    
    with open('results/results.csv', 'a', newline='') as file:
        writetocsv = csv.writer(file)
        writetocsv.writerow(program_run)

    for filename in os.scandir(directory):
        doc = filename
        filepath = directory + "/" + doc.name
  
        prompt = open("prompts/prompt" + str(promptNum) + ".txt", "r").read()
        print(filepath, prompt)

        for i in range(3):
            result_list.append(send_prompt_with_document(filepath, promptNum).content)
            
        # postprocess(testlist, currenttime)
    print(result_list) 

def postprocess(list, currenttime):
    # add timestamp
    file_path = 'results/results.csv'
    with open(file_path, 'a', newline='') as file:
        writetocsv = csv.writer(file)
        writetocsv.writerow(list)

iterate_docs(2)
