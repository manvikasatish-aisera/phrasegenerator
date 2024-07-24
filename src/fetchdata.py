import requests
import json 
from openaigen import *

def no_section_document():
    print("Try another api, document doesn't contain sections")
    print("or document does not exist.")

def retrieve_data(tenant, doc_key, title, source_url):
    utterances = []
    sections_url = f'http://host.docker.internal:8088/tenant-server/v1/tenants/{tenant}/external-documents/retrieve-sections?documentKey={doc_key}&isCommitted=true'
    resp = requests.get(sections_url)

    if resp.status_code != 200:
        no_section_document()

    else:
        re = resp.text
        section_dict = json.loads(re)
        for section in section_dict:
            sect = section['renderContent']
            section_title = section['subject']
            if sect != None:
              utterances = [title, section_title, source_url, send_prompt_with_document(sect, title)]
    return utterances 