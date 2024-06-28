from openai import AzureOpenAI
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader

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

def send_prompt_with_document(filepath, promptNum):
  
  if filepath[-3:] == 'pdf':
    document_text = extractText__pdf(filepath) 
  if filepath[-4:] == 'html':
    document_text = extractText_html(filepath)
  
  title = filepath[filepath.rfind('/')+1 : filepath.rfind('.')]
  
  prompt = open("prompts/prompt" + str(promptNum) + ".txt", "r").read()
  
  #add AzureOpenAi credentials 
  
  completion = client.chat.completions.create(
    model="gpt4",
    temperature = 0.6,
    messages=[
      {"role": "system", "content": '[Document Title] \n"' + title + '"\n\n[Document Content]\n<<' + document_text + ">>\n###\n"},
      {"role": "user", "content": '[Prompt]\n"' + prompt + '"'}
    ]
  )

<<<<<<< HEAD:src/openai-test.py
  return(completion.choices[0].message)
    
print(send_prompt_with_document("/Users/aaravrathi/Desktop/Autopilot.html",2))
=======
  print(completion.choices[0].message)

prompt = open("prompts/prompt1.txt", "r").read()
print(send_prompt_with_document(prompt, "documents/Declaration-of-Independence.pdf"))
>>>>>>> 03652edb9a61093b5fff889cd3ce84b7163c61e3:src/openaigen.py
