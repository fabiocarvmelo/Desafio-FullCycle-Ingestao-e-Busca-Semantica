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

```bash
# 1. Subir o banco de dados:
docker compose up -d

# 2. Executar ingestão do PDF:
python src/ingest.py

# 3. Rodar o chat:
python src/chat.py
```
