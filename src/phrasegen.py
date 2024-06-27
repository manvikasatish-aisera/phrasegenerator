import csv
import os

def iterate_docs():
    directory = "./documents"
    for filename in os.scandir(directory):
        doc = filename

        prompt1 = open("prompts/prompt1.txt", "r")
        content = prompt1.read()

        testlist = call_openai(doc, content)
        postprocess(testlist)

def get_openai_creds():
    return "foo"

def call_openai(doc, prompt):
    get_openai_creds()
    testlist = ["docid", "this is an utterance", "paragraph 2"]
    return testlist

def postprocess(list):
    # add timestamp
    with open('results/results.csv', 'a', newline='') as file:
        writetocsv = csv.writer(file)
        writetocsv.writerow(list)

iterate_docs()