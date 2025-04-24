# DJE Scraping Pipeline

Este projeto realiza o scraping de publicações do Diário de Justiça Eletrônico (DJE), processa os PDFs, extrai informações relevantes utilizando a API Gemini e armazena os dados em um banco de dados PostgreSQL.

## Configuração do Ambiente

1. **Crie o banco de dados no PostgreSQL**:
   Acesse o PostgreSQL e execute o seguinte comando para criar o banco de dados:
   ```sql
   CREATE DATABASE your_database;
   ```

2. **Crie a tabela necessária**:
   Após criar o banco de dados, execute o seguinte comando para criar a tabela:
   ```sql
   CREATE TABLE publicacoes (
       id SERIAL PRIMARY KEY,
       numero_processo VARCHAR(255),
       data_disponibilizacao DATE,
       autores TEXT,
       advogados TEXT,
       valor_principal NUMERIC(15, 2),
       juros_moratorios NUMERIC(15, 2),
       honorarios_adv NUMERIC(15, 2),
       reu TEXT,
       status VARCHAR(50),
       conteudo_publicacao TEXT
   );
   ```

3. **Configure o arquivo `.env`**:
   Crie um arquivo `.env` na raiz do projeto com base no arquivo `.env.example`:
   ```plaintext
   GEMINI_API_KEY=your_gemini_api_key
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   POSTGRES_PASSWORD=your_password
   POSTGRES_USER=your_user
   POSTGRES_DBNAME=your_database
   ```

4. **Instale as dependências**:
   Certifique-se de que você está em um ambiente virtual e execute:
   ```bash
   pip install -r requirements.txt
   ```

5. **Execute o script principal**:
   Inicie o processamento executando:
   ```bash
   python main.py
   ```

## Estrutura do Projeto

- **main.py**: Script principal que orquestra o fluxo do projeto.
- **utils/**: Contém os módulos auxiliares:
  - `fetch_data.py`: Coleta URLs de publicações.
  - `process_pdf.py`: Processa PDFs e extrai texto.
  - `gemini_api.py`: Interage com a API Gemini para extração de dados.
  - `database.py`: Gerencia a conexão e operações no banco de dados.
- **.env**: Arquivo para configurar variáveis de ambiente (não deve ser versionado).
- **.env.example**: Exemplo de configuração para o arquivo `.env`.

## Dependências

As dependências incluem:
- `python-dotenv`: Para carregar variáveis de ambiente do arquivo `.env`.
- `tqdm`: Para exibir barras de progresso no terminal.
- `requests`: Para realizar requisições HTTP.
- `PyPDF2`: Para processar e extrair texto de PDFs.
- `psycopg2-binary`: Para conectar e interagir com o banco de dados PostgreSQL.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença

Este projeto está sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.