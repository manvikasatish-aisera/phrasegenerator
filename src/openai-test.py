from openai import OpenAI
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader

client = OpenAI()

def extractText_html(html_filepath):
  with open(html_filepath, 'r', encoding = 'utf-8') as file:
    soup = BeautifulSoup(file, 'html.parser')
    document_text = soup.get_text()
  return document_text    

def extract_text_from_pdf(pdf_filepath):
    document_text = ''
    reader = PdfReader(pdf_filepath)
    for i in reader.pages:
      text_document = text_document + i.extract_text()
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