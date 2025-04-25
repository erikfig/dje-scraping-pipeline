import requests
import json
from dotenv import load_dotenv
import os
import time
import hashlib
from utils.database import check_hash_existence

load_dotenv()

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key="
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def send_to_gemini(full_text, data_list, max_retries=5):
    hash_value = hashlib.md5(full_text.encode()).hexdigest()

    # Verifica se o hash já existe no banco de dados
    if check_hash_existence(hash_value):
        print("Hash já processado. Ignorando consulta ao Gemini.")
        return

    prompt = f"""
    Com base nesse texto a baixo preencha qual é o modelo a seguir responda somente com o JSON, nada mais, nem formatação nem nada, apenas o json abaixo, como uma api rest e para os valores não encontrados responda com null

    {{
        "numero_processo": "{{---}}",
        "data_disponibilizacao": "{{---}}", # no formato YYYY-MM-DD
        "autores": "{{---}}",
        "advogados": "{{---}}",
        "valor_principal": "{{---}}",
        "juros_moratorios": "{{---}}",
        "honorarios_adv": "{{---}}"
    }}

    Texto:

    {full_text}
    """

    gemini_payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    for attempt in range(max_retries):
        gemini_response = requests.post(f"{GEMINI_API_URL}{GEMINI_API_KEY}", json=gemini_payload)

        if gemini_response.status_code == 200:
            gemini_data = gemini_response.json()
            data = gemini_data['candidates'][0]['content']['parts'][0]['text'].replace("```json", "").replace("```", "").strip()
            data_json = json.loads(data)
            data_json["conteudo_publicacao"] = full_text
            data_json["status"] = "nova"
            data_json["reu"] = "Instituto Nacional do Seguro Social - INSS"
            data_json["hash"] = hash_value
            data_list.append(data_json)
            return
        elif gemini_response.status_code == 429:
            error_data = gemini_response.json()
            retry_delay = 15
            for detail in error_data.get("error", {}).get("details", []):
                if detail.get("@type") == "type.googleapis.com/google.rpc.RetryInfo":
                    retry_delay = int(detail.get("retryDelay", "15s").replace("s", "")) + 2
                    break
            print(f"Limite de requisições excedido. Aguardando {retry_delay} segundos antes de tentar novamente...")
            time.sleep(retry_delay)
        else:
            print(f"Erro na API do Gemini: {gemini_response.status_code}")
            print(gemini_response.text)
            return

    print(f"Falha após {max_retries} tentativas. Não foi possível processar o texto.")
