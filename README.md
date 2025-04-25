# DJE Scraping Pipeline

Este projeto realiza o scraping de publicações do Diário de Justiça Eletrônico (DJE), processa os PDFs, extrai informações relevantes utilizando a API Gemini e armazena os dados em um banco de dados PostgreSQL. Além disso, os dados salvos com sucesso são enviados para uma fila RabbitMQ para processamento posterior.

## Configuração do Ambiente

1. **Crie o banco de dados no PostgreSQL**:
   Acesse o PostgreSQL e execute o seguinte comando para criar o banco de dados:
   ```sql
   CREATE DATABASE your_database;
   ```

2. **Crie as tabelas necessárias**:
   Após criar o banco de dados, execute os seguintes comandos para criar as tabelas:
   ```sql
   CREATE TABLE publications (
       id SERIAL PRIMARY KEY,
       numero_processo TEXT,
       data_disponibilizacao DATE,
       autores TEXT,
       advogados TEXT,
       valor_principal NUMERIC,
       juros_moratorios NUMERIC,
       honorarios_adv NUMERIC,
       reu TEXT,
       status TEXT,
       conteudo_publicacao TEXT
   );

   CREATE TABLE hashes (
       id SERIAL PRIMARY KEY,
       hash TEXT UNIQUE
   );
   ```

3. **Configure o RabbitMQ**:
   Certifique-se de que o RabbitMQ está instalado e em execução. Crie uma fila chamada `publications_queue` (ou o nome configurado no arquivo `.env`).

4. **Configure o arquivo `.env`**:
   Crie um arquivo `.env` na raiz do projeto com base no arquivo `.env.example`:
   ```plaintext
   GEMINI_API_KEY=your_gemini_api_key
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   POSTGRES_PASSWORD=your_password
   POSTGRES_USER=your_user
   POSTGRES_DBNAME=your_database
   RABBITMQ_HOST=localhost
   RABBITMQ_QUEUE=publications_queue
   ```

5. **Instale as dependências**:
   Certifique-se de que você está em um ambiente virtual e execute:
   ```bash
   pip install -r requirements.txt
   ```

6. **Execute o script principal**:
   Inicie o processamento executando:
   ```bash
   python main.py
   ```

## Estrutura do Projeto

- **main.py**: Script principal que orquestra o fluxo do projeto.
- **utils/**: Contém os módulos auxiliares:
  - `fetch_data.py`: Coleta URLs de publicações.
  - `process_pdf.py`: Processa PDFs e extrai texto.
  - `gemini_api.py`: Interage com a API Gemini para extração de dados. Inclui verificação de hash no banco de dados para evitar consultas duplicadas.
  - `database.py`: Gerencia a conexão e operações no banco de dados, além de enviar mensagens para a fila RabbitMQ.
- **.env**: Arquivo para configurar variáveis de ambiente (não deve ser versionado).
- **.env.example**: Exemplo de configuração para o arquivo `.env`.

## Funcionalidades Adicionais

- **Verificação de Hash**: Antes de processar um texto com a API Gemini, o sistema verifica se o hash do texto já existe no banco de dados. Isso evita consultas duplicadas e melhora a eficiência do pipeline.
- **Envio para RabbitMQ**: Após salvar os dados no banco de dados, eles são enviados para uma fila RabbitMQ para processamento posterior.

## Dependências

As dependências incluem:
- `python-dotenv`: Para carregar variáveis de ambiente do arquivo `.env`.
- `tqdm`: Para exibir barras de progresso no terminal.
- `requests`: Para realizar requisições HTTP.
- `PyPDF2`: Para processar e extrair texto de PDFs.
- `psycopg2-binary`: Para conectar e interagir com o banco de dados PostgreSQL.
- `pika`: Para interagir com o RabbitMQ.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença

Este projeto está sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.