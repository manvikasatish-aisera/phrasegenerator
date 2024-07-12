from openai import AzureOpenAI
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
import tiktoken
from numpy import random
import os
from dotenv import load_dotenv

# def extractText_html(html_filepath):
#   with open(html_filepath, 'r', encoding = 'utf-8') as file:
#     soup = BeautifulSoup(file, 'html.parser')
#     document_text = soup.get_text()
#   return document_text    

# def extractText__pdf(pdf_filepath):
#     document_text = ''
#     reader = PdfReader(pdf_filepath)
#     for i in reader.pages:
#       document_text += i.extract_text()
#     return document_text

def count_tokens(text):
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = len(encoding.encode(text))
    return num_tokens

def check_content_length(filetext, prompt, title):
    encoding = tiktoken.get_encoding("cl100k_base")
    expected_count = 8192 - count_tokens(prompt) - count_tokens(title) - count_tokens('[Document Title] \n"' + title + '"\n\n[Document Content]\n<<' + ">>\n###\n" + '[Prompt]\n"' + prompt + '"')
    content = []

    token_count = count_tokens(filetext)
    if token_count > expected_count:
        encoded_text = encoding.encode(filetext)
        
        start_idx = 0
        while start_idx < token_count:
            remaining_tokens = token_count - start_idx
            chunk_size = min(expected_count, remaining_tokens)

            chunk = encoding.decode(encoded_text[start_idx:start_idx + chunk_size])
            content.append(chunk)
            
            start_idx += chunk_size
    else:
        content = [filetext]
    return content
       
def send_prompt_with_document(section, promptNum, title):
  load_dotenv()
  api_version = os.getenv('OPENAI_API_VERSION')
  api_key = os.getenv('OPENAI_API_KEY')
  azure_endpoint = os.getenv('OPENAI_AZURE_ENDPOINT')

  # don't think we need lines 60-63 anymore because the documents are all pretty
  # much HTML, at least the rendered content, have to double check
  # with the other api, but all the ones that are under this api
  # have html text. 

  # if filepath.endswith('.pdf'):
  #   document_text = extractText__pdf(filepath) 
  # if filepath.endswith('.html'):
  #   document_text = extractText_html(filepath)
  
  prompt = open("prompts/prompt" + str(promptNum) + ".txt", "r").read()

  client = AzureOpenAI(
        api_version = api_version,
        api_key = api_key,
        azure_endpoint = azure_endpoint)
  
  # split = check_content_length(document_text, prompt, title)

  # need the check_content_length for documents that have
  # no sections in them

  completion = client.chat.completions.create(
    model = "gpt4",
    temperature = round(random.uniform(0,1), 1),
    messages=[
      {"role": "system", "content": '[Document Title] \n"' + title + '"\n\n[Document Content]\n<<' + section + ">>\n###\n"},
      {"role": "user", "content": '[Prompt]\n"' + prompt + '"'}
    ]
  )
  msg = completion.choices[0].message.content
  
  return msg