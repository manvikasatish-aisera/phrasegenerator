from openai import AzureOpenAI
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
       
def send_prompt_with_document(section, title):
  load_dotenv()
  api_version = os.getenv('OPENAI_API_VERSION')
  api_key = os.getenv('OPENAI_API_KEY')
  azure_endpoint = os.getenv('OPENAI_AZURE_ENDPOINT')
  
  prompt = "Assume the role of a user of a generative AI product. Given the contents of a document and its title, generate a single question, phrase, or statement that is coherent english. The question, statement, or phrase should be short in length, and cover either main ideas, specific details, or implications, and can use slang, short forms of words, etc. Do not include the document title or role of the user in your response. Do not include any escape characters in your response. Each phrase must refer to the main entity in the title or the content text, and be unique and cover something different about the document everytime you generate a new one. Ignore images and HTML tags, and ensure you don't pull phrases straight from the document."

  client = AzureOpenAI(
        api_version = api_version,
        api_key = api_key,
        azure_endpoint = azure_endpoint)

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