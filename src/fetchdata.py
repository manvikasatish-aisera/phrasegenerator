import requests
import fetchdata
import json 
from openaigen import *
import re

def no_section_document():
    print("Try another api, document doesn't contain sections")
    print("or document does not exist.")

def retrieve_data(tenant, botid, doc_key, title, promptNum):
    utterances = []
    sections_url = f'http://localhost:8088/tenant-server/v1/tenants/{tenant}/external-documents/retrieve-sections?documentKey={doc_key}&isCommitted=true'
    resp = requests.get(sections_url)

    if resp.status_code != 200:
        no_section_document()

    else:
        re = resp.text
        section_dict = json.loads(re)
        for section in section_dict:
            sect = section['renderContent']
            if sect != None:
              utterances.append(send_prompt_with_document(sect, promptNum, title))
    return (utterances, title)