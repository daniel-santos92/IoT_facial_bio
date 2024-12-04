import requests
import json
import logging
import os
from dotenv import load_dotenv

load_dotenv()
# Obter a URL do Firebase do ambiente
firebase_url = os.getenv("FIREBASE_URL")
if not firebase_url:
    raise ValueError("FIREBASE_URL não está definida no arquivo .env ou não foi carregada corretamente.")
        
logging.debug(f"Firebase URL carregada: {firebase_url}")

def enviar_dados_firebase(tabela, dados):
    try:
        response = requests.post(f'{firebase_url}/{tabela}/.json', data=json.dumps(dados))
        response.raise_for_status()
        return response.ok
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao enviar dados ao Firebase: {e}")
        return False

def obter_dados_firebase(tabela):
    try:
        response = requests.get(f"{firebase_url}/{tabela}.json")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao acessar Firebase: {e}")
        return None
