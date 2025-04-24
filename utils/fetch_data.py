import requests
import re
import json

URL = "https://dje.tjsp.jus.br/cdje/getListaDeSecoes.do?cdVolume=19&nuDiario=4189&cdCaderno=10"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch_data():
    response = requests.get(URL, headers=HEADERS)
    raw_data = response.content.decode("utf-8")

    json_data = raw_data.replace('"', '')
    json_data = re.sub(r'(\b\w+\b):', r'"\1":', json_data)
    json_data = re.sub(r'\'([\D]*)(")([\D]*)\'', r'""', json_data)
    json_data = json_data.replace("'", '"')
    json_data = re.sub(r'("nmSecao":)"(.*?)"(.*?):', r'\1"\2\3:', json_data)
    json_data = re.sub(r'\s+', '', json_data)
    json_data = re.sub(r'^\[\d+,\[\s*', '[', json_data)
    json_data = re.sub(r'\]\]$', ']', json_data)

    data = json.loads(json_data)

    unique_urls = []
    for item in data:
        url = f"https://dje.tjsp.jus.br/cdje/getPaginaDoDiario.do?cdVolume={item['cdVolume']}&nuDiario={item['nuDiario']}&cdCaderno={item['cdCaderno']}&nuSeqpagina={item['nuSeqpagina']}&uuidCaptcha="
        if url not in unique_urls:
            unique_urls.append(url)

    return unique_urls
