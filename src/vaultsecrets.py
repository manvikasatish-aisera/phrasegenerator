import requests
import os

def authenticate_with_github(vault_address, github_token):
    auth_url = f"{vault_address}/v1/auth/github/login"
    auth_payload = {"token": github_token}
    
    response = requests.post(auth_url, json=auth_payload)
    response.raise_for_status()
    
    client_token = response.json()['auth']['client_token']
    return client_token

def read_secret_from_vault_v1(vault_address, client_token, secret_path):
    headers = {
        'X-Vault-Token': client_token
    }
    
    secret_url = f"{vault_address}/v1/{secret_path}"
    response = requests.get(secret_url, headers=headers)
    response.raise_for_status()
    answer = response.json()
    print(answer)
    return answer

def get_secret_key_v1(vault_address, github_token, secret_path, key):
    client_token = authenticate_with_github(vault_address, github_token)
    secret_data = read_secret_from_vault_v1(vault_address, client_token, secret_path)
    apikey = secret_data['data']['data'][key]
    return apikey

def get_secret_version_v1(vault_address, github_token, secret_path, key):
    client_token = authenticate_with_github(vault_address, github_token)
    secret_data = read_secret_from_vault_v1(vault_address, client_token, secret_path)
    apiversion = secret_data['data']['metadata'][key]
    return apiversion
  
def get_openai_token_from_vault(path, key):
    vault_address = os.getenv('VAULT_ADDR')
    github_token = os.getenv('GITHUB_TOKEN')
    secret_path = path
    if not vault_address:
        raise EnvironmentError("VAULT_ADDR environment variable is not set")
    if not github_token:
        raise EnvironmentError("GITHUB_TOKEN environment variable is not set")
    openaikey = get_secret_key_v1(vault_address, github_token, secret_path, key)  
    return openaikey

def get_openai_version_from_vault(path, key):
    vault_address = os.getenv('VAULT_ADDR')
    github_token = os.getenv('GITHUB_TOKEN')
    secret_path = path
    if not vault_address:
        raise EnvironmentError("VAULT_ADDR environment variable is not set")
    if not github_token:
        raise EnvironmentError("GITHUB_TOKEN environment variable is not set")
    openaiversion = get_secret_version_v1(vault_address, github_token, secret_path, key)  
    return openaiversion