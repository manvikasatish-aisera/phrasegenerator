'''MUST RUN CODE FROM SRC IN DIRECTORY'''

import csv
from openaigen import *
from fetchdata import * 
from S3export import *
import openpyxl
import requests
import os

cluster = os.getenv('CLUSTER').lower()
tenant = os.getenv('TENANT')
bot = os.getenv('BOT_ID')
num_docs = int(os.getenv('NUM_DOCS'))
host_ip = os.getenv('HOST_IP')

# now = datetime.now()
date_time = os.getenv('TODAY')

print("--------------------")
print("Environment:", cluster)
print("Tenant:", tenant)
print("Source bot_id:", bot)
print("Date: ", date_time)

def iterate_docs(cluster, tenant, bot):
    if not os.path.isfile(f'/logs/Info_cluster{cluster}_tenant{tenant}_botid{bot}.csv'):
        if not getDocKeys(tenant, bot):
            print("Incorrect combination of cluster/tenant/bot... Try again.")
            raise SystemExit
        # reconsider printing this
        print("First time accessing this bot, gathering all documents...")

    print("iterating through the docs")

    with open(f'/logs/Info_cluster{cluster}_tenant{tenant}_botid{bot}.csv') as file_obj:
        row_count = 0 
        reader_obj = csv.reader(file_obj) 
        
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        
        for row in reader_obj: 
            doc_key = int(row[0])
            source_url = row[1]
            title = row[2]
            section_url = f'http://{host_ip}:8088/tenant-server/v1/tenants/{tenant}/external-documents/retrieve-sections?documentKey={doc_key}&isCommitted=true'
            response = requests.get(section_url)

            if response.status_code == 200:
                if title is None:
                    title = f'No Title. Document Key: {doc_key}'
                if source_url is None:
                    source_url = f'No URL. Document Key: {doc_key}'

                utterances = retrieve_data(tenant, doc_key, title, source_url, host_ip)
                
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

def getDocKeys(tenant, botid):
    try:
        url = f"http://{host_ip}:8088/tenant-server/v1/tenants/{tenant}/external-documents/check-health?botId={botid}"
        response = json.loads(requests.get(url).text)
        print("Retrieved keys!!!")
    except:
        print("Failed to retrieve keys... :(")
        return False
    
    file_path = f"/logs/Info_cluster{cluster}_tenant{tenant}_botid{botid}.csv"
    directory = os.path.dirname(file_path)

    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(file_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for item in response:
            csvwriter.writerow([item.get("documentKey"), item.get("source"), item.get("title")])

    return True

print("...")
iterate_docs(cluster, tenant, bot)