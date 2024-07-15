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

def get_document_key(dict, doc_title):
    doc_key = 0
    for dic in dict:
        if dic['title'] == doc_title:
            doc_key = dic['documentKey']
            break
    return doc_key

# will modify once i get access to the API
def no_section_document():
    print("Try another api, document doesn't contain sections")
    print("or document does not exist.")

def retrieve_data(promptNum):
    utterances = []
    # right now its uat
    tenant = input('Tenant: ')
    botid = input('Bot ID: ')

    # up for change
    num_docs = 25 

    document_url = f'http://localhost:8088/tenant-server/v1/tenants/{tenant}/external-documents/check-health?botId={botid}' 
    response = requests.get(document_url)

    # implement better error handling, throw exceptions instead of print statements. fix this section
    # if response.status_code != 200:
    #     print("cluster, tenant, or bot id does not exist or is incorrect. Please try again.")

    resp_text = response.text
    dict = json.loads(resp_text)
    for dic in dict:
        print(dic)

    print(len(dict))

    doc_key = int(input('Document Key: '))

    doc_title = get_doc_title(dict, doc_key)

    sections_url = f'http://localhost:8088/tenant-server/v1/tenants/{tenant}/external-documents/retrieve-sections?documentKey={doc_key}&isCommitted=true'
    resp = requests.get(sections_url)

    if resp.status_code != 200:
        # no sections found in the document, try another api
        numPhrases = input('Number of Phrases: ')
        no_section_document()

    else:
        numPhrases = input('Number of Phrases (per section): ')
        re = resp.text
        section_dict = json.loads(re)
        for section in section_dict:
            sect = section['renderContent']
            if sect != None:
              utterances.append(send_prompt_with_document(sect, promptNum, doc_title))
    return (utterances, doc_title)