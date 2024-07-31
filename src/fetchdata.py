import requests
import json
from openaigen import *

def no_section_document():
   # Prints a message indicating that the document does not contain sections.
    print("Document does not contain sections...")

def retrieve_data(tenant, doc_key, title, source_url, host_ip):
    """
    Retrieve data from document sections for a given tenant and document key.

    Args:
        tenant (str): The tenant identifier.
        doc_key (int): The document key.
        title (str): The document title.
        source_url (str): The source URL of the document.
        host_ip (str): The host IP address.

    Returns:
        list: A list of utterances, where each utterance is a list containing 
              the document title, section title, source URL, and the processed content.
    """
    
    utterances = []
    sections_url = f'http://{host_ip}:8088/tenant-server/v1/tenants/{tenant}/external-documents/retrieve-sections?documentKey={doc_key}&isCommitted=true'
    
    try:
        # Send a GET request to retrieve the document sections
        resp = requests.get(sections_url)
        
        # Check if the response status code is not 200
        if resp.status_code != 200:
            no_section_document()
            return utterances
        
        # Parse the JSON response
        section_dict = json.loads(resp.text)
    except requests.RequestException as e:
        # Handle any request exceptions (network issues, invalid URL, etc.)
        print(f"Failed to retrieve sections for document key {doc_key}: {e}")
        return utterances
    except json.JSONDecodeError:
        # Handle JSON parsing errors
        print(f"Failed to parse JSON response for document key {doc_key}")
        return utterances

    # Iterate through each section in the parsed JSON response
    for section in section_dict:
        sect = section.get('renderContent')
        section_title = section.get('subject')

        if sect is not None:
            # Process the content and create a list with the required data
            processed_content = send_prompt_with_document(sect, title)
            set1 = [title, section_title, source_url, processed_content]
            utterances.append(set1)
    
    return utterances
