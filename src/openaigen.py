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
      text_document = text_document + i.extract_text()
    return document_text

def send_prompt_with_document(filepath, promptNum):
  if filepath.endswith('.pdf'):
    document_text = extractText__pdf(filepath) 
  if filepath.endswith('.html'):
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

  return(completion.choices[0].message)
    
print(send_prompt_with_document("./documents/Tesla_Autopilot.htm",2))
