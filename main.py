from utils.fetch_data import fetch_data
from utils.process_pdf import process_pdf
from utils.gemini_api import send_to_gemini
from utils.database import save_data
from tqdm import tqdm

def main():
    unique_urls = fetch_data()
    data_list = []

    for url in tqdm(unique_urls, desc="Processando PDFs"):
        full_text = process_pdf(url)
        send_to_gemini(full_text, data_list)

    for data in tqdm(data_list, desc="Salvando no banco de dados"):
        save_data(data)

if __name__ == "__main__":
    main()

