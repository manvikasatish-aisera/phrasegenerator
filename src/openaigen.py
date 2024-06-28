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

def send_prompt_with_document(prompt, document_text):
  combined_prompt = prompt + "\n\nDocument:\n" + document_text + "\n###\n"
  
  client = OpenAI()
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    temperature = 0.6,
    messages=[
      {"role": "system", "content": "\n\nDocument:\n" + document_text + "\n###\n"},
      {"role": "user", "content": prompt}
    ]
  )

  print(completion.choices[0].message)

prompt = open("prompts/prompt1.txt", "r").read()
print(send_prompt_with_document(prompt, "documents/Declaration-of-Independence.pdf"))