import openai
from openai import AzureOpenAI
import tiktoken
from numpy import random
from vaultsecrets import *
from dotenv import load_dotenv

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
  apikeyPath = "/qa/data/environment/common/openai"

  api_key = get_openai_token_from_vault(apikeyPath, "OPENAI_API_KEY")
  api_version = get_openai_version_from_vault(apikeyPath, "version")
  azure_endpoint = os.getenv('OPENAI_AZURE_ENDPOINT')
  
  prompt = "Assume the role of a user of a generative AI product. Given the contents of a document and its title, generate a single question, phrase, or statement that is coherent english. The question, statement, or phrase should be short in length, and cover either main ideas, specific details, or implications, and can use slang, short forms of words, etc. Do not include the document title or role of the user in your response. Do not include any escape characters in your response. Each phrase must refer to the main entity in the title or the content text, and be unique and cover something different about the document everytime you generate a new one. Ignore images and HTML tags, and ensure you don't pull phrases straight from the document."

  client = AzureOpenAI(
        api_key = api_key,
        api_version = api_version,
        azure_endpoint = azure_endpoint)
  
  try:
      completion = client.chat.completions.create(
      model = "gpt4",
      temperature = round(random.uniform(0,1), 1),
      messages=[
        {"role": "system", "content": '[Document Title] \n"' + title + '"\n\n[Document Content]\n<<' + section + ">>\n###\n"},
        {"role": "user", "content": '[Prompt]\n"' + prompt + '"'}
      ]
      )
      msg = completion.choices[0].message.content
  except openai.error.OpenAIError as e:
    print(f"Error occurred: {e}")
    raise

  
  return msg
