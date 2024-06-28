from openai import AzureOpenAI
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
import tiktoken

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
       p1, p2 = filetext.split(' ', 1)
       content = [p1, p2]
    content = [filetext]
    return content
       
def send_prompt_with_document(filepath, promptNum):
  if filepath.endswith('.pdf'):
    document_text = extractText__pdf(filepath) 
  if filepath.endswith('.html'):
    document_text = extractText_html(filepath)
  
  title = filepath[filepath.rfind('/')+1 : filepath.rfind('.')]
  
  prompt = open("prompts/prompt" + str(promptNum) + ".txt", "r").read()

  completion = client.chat.completions.create(
    model="gpt4",
    temperature = 0.6,
    messages=[
      {"role": "system", "content": '[Document Title] \n"' + title + '"\n\n[Document Content]\n<<' + document_text + ">>\n###\n"},
      {"role": "user", "content": '[Prompt]\n"' + prompt + '"'}
    ]
  )

  return(completion.choices)
    
for i in range(3):  
  print(send_prompt_with_document("documents/FAQ _ GeForce.html",2)[i].message.content)
