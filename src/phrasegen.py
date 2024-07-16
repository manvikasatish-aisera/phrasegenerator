import csv
import os
from datetime import datetime
from openaigen import *
from fetchdata import * 
import openpyxl
import requests
import boto3

def iterate_docs(promptNum):
    # cluster = input('Cluster: ')
    tenant = 10000
    bot = 740
    currenttime = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    csv_file = os.path.join("results",f"csvResults-{currenttime}.csv")

    with open('src/documentKeys.csv') as file_obj:
        row_count = 0 
        reader_obj = csv.reader(file_obj) 
        # Iterate over each row in the csv  
        # file using reader object 
        row_count = 0
        for row in reader_obj: 
            doc_key = int(row[0])
            section_url = f'http://localhost:8088/tenant-server/v1/tenants/{tenant}/external-documents/retrieve-sections?documentKey={doc_key}&isCommitted=true'
            response = requests.get(section_url)
            print(response.status_code)
            if response.status_code == 200:
                print(doc_key)
                utterances = retrieve_data(tenant, bot, doc_key, promptNum)
                postprocess(utterances, csv_file)
                row_count += 1
            if row_count >= 25:
                print('bye')
                break
                
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    if sheet['A1'].value == None:
        sheet.cell(sheet.max_row,1,utterances[1])
    else:
        sheet.cell(sheet.max_row+1,1,utterances[1])
                        
    for i in range(len(utterances[0])):
        sheet.cell(sheet.max_row,i+2,utterances[0][i])
                        
    workbook.save(f"results/excelResults-{currenttime}.xlsx")
            

    # utterances = retrieve_data(promptNum)

    # s3 = boto3.client('s3')
    # s3.meta.client.upload_file('/tmp/hello.txt', 'mybucket', 'hello.txt')

    # s3.upload_file(
    #     Filename="C:/Users/admin/Desktop/gfg_logo.png",
    #     Bucket="mygfgbucket",
    #     Key="firstgfgbucket.png"
    # )

    # currenttime = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    # csv_file = os.path.join("results",f"csvResults-{currenttime}.csv")
    
    # workbook = openpyxl.Workbook()
    # sheet = workbook.active

    # postprocess(utterances,csv_file)
        
    # if sheet['A1'].value == None:
    #     sheet.cell(sheet.max_row,1,utterances[1])
    # else:
    #     sheet.cell(sheet.max_row+1,1,utterances[1])
            
    # for i in range(len(utterances[0])):
    #     sheet.cell(sheet.max_row,i+2,utterances[0][i])
            
    # workbook.save(f"results/excelResults-{currenttime}.xlsx")

def postprocess(list,csvfile):
    with open(csvfile, 'a', newline='') as file:
        writetocsv = csv.writer(file)
        writetocsv.writerow(list)

promptNum = 4
iterate_docs(promptNum)