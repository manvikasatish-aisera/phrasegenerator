'''MUST RUN CODE FROM SRC IN DIRECTORY'''

import csv
from openaigen import *
from fetchdata import * 
from S3export import *
import openpyxl
import requests
import subprocess
import time
import os

cluster = os.getenv('CLUSTER')
tenant = os.getenv('TENANT')
bot = os.getenv('BOT_ID')
num_docs = int(os.getenv('NUM_DOCS'))
port_number = int(os.getenv('PORT_NUM'))
#date_time = sys.argv[4]

now = datetime.now()
date_time = now.strftime("%Y_%m_%d_%H_%M")

print("--------------------")
print("Environment:", cluster)
print("Tenant:", tenant)
print("Source bot_id:", bot)
print("Date: ", date_time)

def iterate_docs(cluster, tenant, bot):
    # numDocs = 3
    if not os.path.isfile(f'../documentInfo/Info_cluster{cluster}_tenant{tenant}_botid{bot}.csv'):
        if not getDocKeys(tenant, bot):
            print("incorrect combo of cluster/tenant/bot")
            raise SystemExit
        print("First time accessing this bot, gathering all documents...")

    docs = retrieve_docs(tenant, bot)
    print("iterating through the docs")
    with open(f'../documentInfo/Info_cluster{cluster}_tenant{tenant}_botid{bot}.csv') as file_obj:
        row_count = 0 
        reader_obj = csv.reader(file_obj) 
        
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        
        for row in reader_obj: 
            doc_key = int(row[0])
            source_url = row[1]
            title = row[2]
            section_url = f'http://host.docker.internal:{port_number}/tenant-server/v1/tenants/{tenant}/external-documents/retrieve-sections?documentKey={doc_key}&isCommitted=true'
            response = requests.get(section_url)

            if response.status_code == 200:
                if title is None:
                    title = f'No Title. Document Key: {doc_key}'
                if source_url is None:
                    source_url = f'No URL. Document Key: {doc_key}'

                utterances = retrieve_data(tenant, doc_key, title, source_url, port_number)
                
                for i in range(len(utterances)):
                    start_row = sheet.max_row + 1
                    for col_index, item in enumerate(utterances[i],start=1):
                        sheet.cell(row=start_row,column=col_index,value=item)
                        
                row_count += 1
            if row_count >= num_docs:
                break
            
        sheet.cell(1,1,"Doc Title")
        sheet.cell(1,2,"Section Title")
        sheet.cell(1,3,"URL")
        sheet.cell(1,4,"Utterance/Phrase")
        
        workbook.save(f"../results/{cluster}_tenant{tenant}_botid{bot}_excel_{date_time}.xlsx")        
        uploadFile_to_S3(cluster, tenant, bot)
    
def retrieve_docs(tenant, botid):
    print("retrieving the docs")
    document_url = f'http://host.docker.internal:{port_number}/tenant-server/v1/tenants/{tenant}/external-documents/check-health?botId={botid}' 
    response = requests.get(document_url)
    response_text = response.text
    dict = json.loads(response_text)

    return dict

def get_doc_title_and_source(docs, doc_key):
    doc_title = ''
    for doc in docs:
        if doc['documentKey'] == doc_key:
            doc_title = doc['title']
            source_url = doc['source']
            break
    return doc_title, source_url


def postprocess(list,csvfile):
    with open(csvfile, 'a', newline='') as file:
        writetocsv = csv.writer(file)
        writetocsv.writerow(list)

def getDocKeys(tenant,botid):
    try:
        response = json.loads(requests.get(f"http://host.docker.internal:{port_number}/tenant-server/v1/tenants/{tenant}/external-documents/check-health?botId={botid}").text)
    except:
        return False
    file_path = f"../documentInfo/Info_cluster{cluster}_tenant{tenant}_botid{botid}.csv"
    with open(file_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for item in response:
            csvwriter.writerow([item.get("documentKey") , item.get("source") , item.get("title")])
    return True

# run_kube_commands(cluster)
print("...")
iterate_docs(cluster, tenant, bot)