import csv
import os
import datetime
import pandas as pd

def iterate_docs():
    directory = "./documents"
    currenttime = datetime.datetime.now()

    program_run = ["program run time", currenttime]
    with open('results/results.csv', 'a', newline='') as file:
        writetocsv = csv.writer(file)
        writetocsv.writerow(program_run)

    for filename in os.scandir(directory):
        doc = filename

        prompt1 = open("prompts/prompt1.txt", "r")
        content = prompt1.read()

        testlist = call_openai(doc, content)
        postprocess(testlist, currenttime)

def get_openai_creds():
    return "foo"

def call_openai(doc, prompt):
    get_openai_creds()
    testlist = ["doc id", "this is an utterance", "paragraph 2"]
    return testlist

def postprocess(list, currenttime):
    # add timestamp
    file_path = 'results/results.csv'
    with open(file_path, 'a', newline='') as file:
        writetocsv = csv.writer(file)
        writetocsv.writerow(list)
    csvtoexcel(file_path)

def csvtoexcel(csvfile):
    df_new = pd.read_csv(csvfile)
    GFG = pd.ExcelWriter('results/results.xlsx')
    df_new.to_excel(GFG, index=False, header=True)
    GFG.close()
    
iterate_docs()
