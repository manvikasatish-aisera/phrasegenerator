import csv
import os
from datetime import datetime
from openaigen import *
from fetchdata import * 
import openpyxl
import boto3

def iterate_docs(promptNum):
    cluster = input('Cluster: ')
    utterances = retrieve_data(promptNum)

    s3 = boto3.client('s3')
    # s3.meta.client.upload_file('/tmp/hello.txt', 'mybucket', 'hello.txt')

    # s3.upload_file(
    #     Filename="C:/Users/admin/Desktop/gfg_logo.png",
    #     Bucket="mygfgbucket",
    #     Key="firstgfgbucket.png"
    # )

    currenttime = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    csv_file = os.path.join("results",f"csvResults-{currenttime}.csv")
    
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    postprocess(utterances,csv_file)
        
    if sheet['A1'].value == None:
        sheet.cell(sheet.max_row,1,utterances[1])
    else:
        sheet.cell(sheet.max_row+1,1,utterances[1])
            
    for i in range(len(utterances[0])):
        sheet.cell(sheet.max_row,i+2,utterances[0][i])
            
    workbook.save(f"results/excelResults-{currenttime}.xlsx")

def postprocess(list,csvfile):
    with open(csvfile, 'a', newline='') as file:
        writetocsv = csv.writer(file)
        writetocsv.writerow(list)

promptNum = 4
iterate_docs(promptNum)
