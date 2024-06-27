import csv
import os

def iterate_docs():
    directory = "documents"
    for filename in os.scandir(directory):
        doc = filename

        prompt1 = open("prompt1.txt", "r")
        content = prompt1.read()

        testlist = call_openai(doc, content)
        postprocess(testlist)

def get_openai_creds():
    return "foo"

def call_openai(doc, prompt):
    get_openai_creds()
    testlist = []
    return testlist

def postprocess(list):
    with open('results.csv', 'a', newline='') as file:
        writetocsv = csv.writer(file)
        writetocsv.writerow(list)