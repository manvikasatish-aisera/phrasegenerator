import csv
import os
from datetime import datetime
from openaigen import *
from fetchdata import * 
import openpyxl
import requests

def iterate_docs(cluster, tenant, bot):
    promptNum = 4

    docs = retrieve_docs(tenant, bot)

    currenttime = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    csv_file = os.path.join("../results",f"{cluster}_tenant{tenant}_botid{bot}_csv_{currenttime}.csv")

    with open('documentKeys.csv') as file_obj:
        row_count = 0 
        reader_obj = csv.reader(file_obj) 

        for row in reader_obj: 
            doc_key = int(row[0])
            section_url = f'http://localhost:8088/tenant-server/v1/tenants/{tenant}/external-documents/retrieve-sections?documentKey={doc_key}&isCommitted=true'
            response = requests.get(section_url)

            if response.status_code == 200:
                title = get_doc_title(docs, doc_key)
                if title is None:
                    title = f'No Title. Document Key: {doc_key}'
                print(title, doc_key)
                utterances = retrieve_data(tenant, bot, doc_key, title, promptNum)
                postprocess(utterances, csv_file)
                row_count += 1
            if row_count >= 25:
                break
                
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    if sheet['A1'].value == None:
        sheet.cell(sheet.max_row,1,utterances[1])
    else:
        sheet.cell(sheet.max_row+1,1,utterances[1])
                        
    for i in range(len(utterances[0])):
        sheet.cell(sheet.max_row,i+2,utterances[0][i])
                        
    workbook.save(f"results/{cluster}_tenant{tenant}_botid{bot}_excel_{currenttime}.xlsx")

def retrieve_docs(tenant, botid):
 document_url = f'http://localhost:8088/tenant-server/v1/tenants/{tenant}/external-documents/check-health?botId={botid}&limit=25' 
 response = requests.get(document_url)
 response_text = response.text
 dict = json.loads(response_text)
 print(len(dict))

 return dict

def get_doc_title(docs, doc_key):
    doc_title = ''
    for doc in docs:
        if doc['documentKey'] == doc_key:
            doc_title = doc['title']
            break
    return doc_title

def postprocess(list,csvfile):
    with open(csvfile, 'a', newline='') as file:
        writetocsv = csv.writer(file)
        writetocsv.writerow(list)


iterate_docs('uat', 10000, 740)