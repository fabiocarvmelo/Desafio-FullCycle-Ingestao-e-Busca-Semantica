import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_postgres import PGVector
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

pg_url = os.getenv("DATABASE_URL")
pg_collection_name = os.getenv("PG_VECTOR_COLLECTION_NAME")

# essa função é uma estpécie de "fábrica" que monta e retorna o chain de busca
# para usar basta chamar: 
#   search_prompt().invoke(pergunta="conteúdo da pergunta")
def search_prompt():
    try:
        # confirma se as variáveis de ambiente estão setadas
        if not pg_url or not pg_collection_name:
            raise RuntimeError("As variáveis de ambiente DATABASE_URL e PG_VECTOR_COLLECTION_NAME não foram configuradas")
        
        # configura a conexão com o banco de dados
        embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL","text-embedding-3-small"))
        
        store = PGVector(
            embeddings=embeddings,
            collection_name=pg_collection_name,
            connection=pg_url,
            use_jsonb=True,
        )
        
        # configura um "recuperador" para buscar os 10 pedaços mais relevantes
        retriever = store.as_retriever(search_kwargs={"k": 10})

        # inicializa o modelo da OpenAI
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

        # cria a definição do prompt
        prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

        # constroi o chain de busca
        chain = (
            {"contexto": retriever, "pergunta": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

        return chain
    except Exception as e:
        print(f"Erro ao inicializar search_prompt: {e}")
        return None
  