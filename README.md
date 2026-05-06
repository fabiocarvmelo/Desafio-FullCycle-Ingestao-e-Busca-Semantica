# Desafio MBA Engenharia de Software com IA - Full Cycle

---
# Executando o projeto

## Como inicializar o ambiente local:

Após clonar o projeto, execute:

```bash
python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
``` 

## Como executar o projeto:

1. Configure o arquivo .env, informando o DATABASE_URL, PG_VECTOR_COLLECTION_NAME e a chave da OpenIA. 
Obs.: A PDF_PATH é opcional, se executar a partir da pasta principal do projeto, o script captura o arquivo que está no repositório. 

2. Execute no terminal os comandos:

```bash
# 1. Subir o banco de dados:
docker compose up -d

# 2. Executar ingestão do PDF:
python src/ingest.py

# 3. Rodar o chat:
python src/chat.py
```
3. o chat.py entra em um looping, onde poderá testar diversas perguntas, uma seguida da outra