import requests
import fetchdata
import json 
from openaigen import *
import re

def get_doc_title(dict, doc_key):
    doc_title = ''
    for dic in dict:
        if dic['documentKey'] == doc_key:
            doc_title = dic['title']
            break
    return doc_title

def no_section_document():
    print("Try another api, document doesn't contain sections")

def retrieve_data(promptNum):
    utterances = []
    tenant = input('Tenant: ')
    botid = input('Bot ID: ')

    document_url = f'http://localhost:8088/tenant-server/v1/tenants/{tenant}/external-documents/check-health?botId={botid}' 
    response = requests.get(document_url)

    resp_text = response.text
    dict = json.loads(resp_text)
    doc_key = int(input('Document Key: '))
    doc_title = get_doc_title(dict, doc_key)

    section_url = f'http://localhost:8088/tenant-server/v1/tenants/{tenant}/external-documents/retrieve-sections?documentKey={doc_key}&isCommitted=true'
    resp = requests.get(section_url)

    if resp.status_code != 200:
        # no sections found in the document, try another api
        no_section_document()
    else:
        re = resp.text
        section_dict = json.loads(re)
        for section in section_dict:
            sect = section['renderContent']
            if sect != None:
              utterances.append(send_prompt_with_document(sect, promptNum, doc_title))
    return (utterances, doc_title)