import csv
import os
import datetime
from openaigen import *

def iterate_docs():
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

        prompt = open("prompts/prompt1.txt", "r").read()
        print(filepath, prompt)
        # print(send_prompt_with_document(prompt, filepath))

        # result_list.append(send_prompt_with_document(prompt, filepath))
        # testlist = call_openai(doc, prompt)
        # postprocess(testlist, currenttime)
    print(result_list) 

def postprocess(list, currenttime):
    # add timestamp
    file_path = 'results/results.csv'
    with open(file_path, 'a', newline='') as file:
        writetocsv = csv.writer(file)
        writetocsv.writerow(list)

iterate_docs()
