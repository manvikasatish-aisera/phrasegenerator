from openai import AzureOpenAI
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
import tiktoken
from numpy import random
import os
from dotenv import load_dotenv

def extractText_html(html_filepath):
  with open(html_filepath, 'r', encoding = 'utf-8') as file:
    soup = BeautifulSoup(file, 'html.parser')
    document_text = soup.get_text()
  return document_text    

def extractText__pdf(pdf_filepath):
    document_text = ''
    reader = PdfReader(pdf_filepath)
    for i in reader.pages:
      document_text += i.extract_text()
    return document_text

def count_tokens(text):
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = len(encoding.encode(text))
    return num_tokens

def check_content_length(filetext):
    expected_count = 8192
    content = []

    token_count = count_tokens(filetext)
    if token_count > expected_count:
        encoding = tiktoken.get_encoding("cl100k_base")
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
       
def send_prompt_with_document(filepath, promptNum):
  load_dotenv()
  api_version = os.getenv('OPENAI_API_VERSION')
  api_key = os.getenv('OPENAI_API_KEY')
  azure_endpoint = os.getenv('OPENAI_AZURE_ENDPOINT')

  if filepath.endswith('.pdf'):
    document_text = extractText__pdf(filepath) 
  if filepath.endswith('.html'):
    document_text = extractText_html(filepath)
  
  title = filepath[filepath.rfind('/')+1 : filepath.rfind('.')]
  prompt = open("prompts/prompt" + str(promptNum) + ".txt", "r").read()
  
  client = AzureOpenAI(
        api_version = api_version,
        api_key = api_key,
        azure_endpoint = azure_endpoint)

  completion = client.chat.completions.create(
      model = "gpt4",
      temperature = round(random.uniform(0,2),1),
      messages=[
        {"role": "system", "content": '[Document Title] \n"' + title + '"\n\n[Document Content]\n<<' + document_text + ">>\n###\n"},
        {"role": "user", "content": '[Prompt]\n"' + prompt + '"'}
      ]
  )

  return(completion.choices[0].message.content)

print(send_prompt_with_document("documents/Frequently Asked Questions_ Windows 10 - Microsoft Community.html", 2))