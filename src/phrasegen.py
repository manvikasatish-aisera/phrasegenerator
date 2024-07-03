import csv
import os
from datetime import datetime
from openaigen import *
import openpyxl



def iterate_docs(promptNum):
    directory = "./documents"
    
    currenttime = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    csv_file = os.path.join("results",f"csvResults-{currenttime}.csv")
    
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    for filename in os.scandir(directory):
        doc = filename
        filepath = directory + "/" + doc.name
        utterances = send_prompt_with_document(filepath, promptNum)
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
        
    
    

iterate_docs(3)
