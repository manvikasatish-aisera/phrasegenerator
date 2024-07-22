import csv
#import os
#from datetime import datetime
from openaigen import *
from fetchdata import * 
from S3export import *
import openpyxl
import requests
import sys
import subprocess
import time

print("got to this point.")
cluster = sys.argv[1]
tenant = sys.argv[2]
bot = sys.argv[3]
#date_time = sys.argv[4]

now = datetime.now()
date_time = now.strftime("%Y_%m_%d_%H_%M")

print("Environment:", cluster)
print("Tenant:", tenant)
print("Source bot_id:", bot)
print("Date: ", date_time)

def run_kube_commands(env):
    print("running kube commands")
    port_forward_db_command = "kubectl port-forward service/tenant-server 8088:8088 &"
    context_command = None

    if env in ["dev0", "dev2", "dev4", "dev6", "uat"]:
        context_command = "kubectl config use-context aws-007"
        namespace_command = "kubens " + env

    elif env in ["staging0", "poc0"]:
        context_command = "kubectl config use-context aws-hood-stg"
        namespace_command = "kubens " + env

    elif env == "prod0" :
        context_command = "kubectl config use-context aws-hood-prod"
        namespace_command = "kubens " + env

    elif env == "prod1" :
        context_command = "kubectl config use-context aws-hood-prod1"
        namespace_command = "kubens " + env

    elif env == "azure-prod" :
        context_command = "kubectl config use-context aisera-katmai-prod-aks"
        namespace_command = "kubens prod"

    # Kill any existing kubectl process
    subprocess.run("pkill kubectl", shell=True)

    subprocess.run(context_command, shell=True, check=True)
    subprocess.run(namespace_command, shell=True, check=True)
    subprocess.run(port_forward_db_command, shell=True, check=True)
    print("done portforwarding")
    time.sleep(5)


def iterate_docs(cluster, tenant, bot):
    numDocs = 5
    
    if not os.path.isfile(f'./documentKeys/Keys_cluster{cluster}_tenant{tenant}_botid{bot}.csv'):
        if not getDocKeys(tenant, bot):
            print("incorrect combo of cluster/tenant/bot")
            raise SystemExit
        print("First time accessing this bot, gathering all documents...")

    docs = retrieve_docs(tenant, bot)
    print("iterating through the docs")
    with open('./src/documentKeys.csv') as file_obj:
        row_count = 0 
        reader_obj = csv.reader(file_obj) 
        
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        
        for row in reader_obj: 
            doc_key = int(row[0])
            section_url = f'http://localhost:8088/tenant-server/v1/tenants/{tenant}/external-documents/retrieve-sections?documentKey={doc_key}&isCommitted=true'
            response = requests.get(section_url)

            if response.status_code == 200:
                title, source_url = get_doc_title_and_source(docs, doc_key)
                if title is None:
                    title = f'No Title. Document Key: {doc_key}'
                if source_url is None:
                    source_url = f'No URL. Document Key: {doc_key}'

                utterances = retrieve_data(tenant, doc_key, title, source_url)
                
                start_row = 1 if sheet.max_row == 1 else sheet.max_row + 1
                for i in range(len(utterances)):
                    for col_index, item in enumerate(utterances[i],start=1):
                        sheet.cell(row=start_row,column=col_index,value=item)
                        
                row_count += 1
            if row_count >= numDocs:
                break
            
        sheet.cell(1,1,"Doc Title")
        sheet.cell(1,2,"Section Title")
        sheet.cell(1,3,"URL")
        sheet.cell(1,4,"Utterance/Phrase")
        
        workbook.save(f"./results/{cluster}_tenant{tenant}_botid{bot}_excel_{date_time}.xlsx")        
        uploadFile_to_S3(cluster, tenant, bot)
    
def retrieve_docs(tenant, botid):
 print("retrieving the docs")
 document_url = f'http://localhost:8088/tenant-server/v1/tenants/{tenant}/external-documents/check-health?botId={botid}' 
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
        response = json.loads(requests.get(f"http://localhost:8088/tenant-server/v1/tenants/{tenant}/external-documents/check-health?botId={botid}").text)
    except:
        return False
    file_path = f"scripts/Phrase_Generator/documentKeys/Keys_clusteruat_tenant{tenant}_botid{botid}.csv"
    with open(file_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for item in response:
            csvwriter.writerow([item.get("documentKey")])
    return True


print("starting portforwarding")
run_kube_commands(cluster)
print("...")
iterate_docs(cluster, tenant, bot)