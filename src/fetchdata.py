import requests
#import fetchdata
import json 
from openaigen import *


def no_section_document():
    print("Try another api, document doesn't contain sections")
    print("or document does not exist.")

def retrieve_data(tenant, doc_key, title, source_url):
    utterances = []
    sections_url = f'http://localhost:8088/tenant-server/v1/tenants/{tenant}/external-documents/retrieve-sections?documentKey={doc_key}&isCommitted=true'
    resp = requests.get(sections_url)

    if resp.status_code != 200:
        no_section_document()

    else:
        section_dict = json.loads(resp.text)
        for section in section_dict:
            sect = section['renderContent']
            section_title = section['subject']
            if sect != None:
              set1 = [title, section_title, source_url, send_prompt_with_document(sect, title)]
              utterances.append(set1)
    return utterances 