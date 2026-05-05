import os
from pathlib import Path
from dotenv import load_dotenv

# componentes do LangChain
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
#from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from langchain_postgres import PGVector

load_dotenv()

pdf_path = os.getenv("PDF_PATH")
pg_url = os.getenv("DATABASE_URL")
pg_collection_name = os.getenv("PG_VECTOR_COLLECTION_NAME")

if not pdf_path:
    # força carregando o PDF que está uma pasta acima do script atual
    print("A variável de ambiente PDF_PATH não foi configurada. Tentando carregar o PDF da pasta local...")
    current_dir = Path(__file__).parent.parent
    pdf_path = current_dir / "document.pdf"

def ingest_pdf():
    # valida se o arquivo existe
    if not pdf_path or not Path(pdf_path).exists():
        raise RuntimeError(f"O arquivo {pdf_path} não foi encontrado")

    # valida se as variáveis do PGVector estão setadas
    if not pg_url or not pg_collection_name:
        raise RuntimeError("As variáveis de ambiente DATABASE_URL e PG_VECTOR_COLLECTION_NAME não foram configuradas")

    print(f" --- Iniciando ingestão do PDF: {pdf_path} ---")

    # carrega o PDF
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    print(f"PDF carregado com sucesso. Total de páginas: {len(documents)}")

    # fatia em pedaçoes menores
    splits = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=150,
        add_start_index=True
        ).split_documents(documents)
    print(f"PDF dividido em {len(splits)} pedaços")

    # remove os campos vazios para evitar erros na hora de incluir na base de dados
    enriched_docs = [
        Document(
            page_content=doc.page_content,
            metadata={
                k: v for k, v in doc.metadata.items() if v not in ("", None)
            }
        )
        for doc in splits
    ]

    # inicializa os embeddings e VectorStore
    embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL","text-embedding-3-small"))
    #embeddings = GoogleGenerativeAIEmbeddings(model="embedding-001")

    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=pg_collection_name,
        connection=pg_url,
        use_jsonb=True
    )

    # envia para o banco de dados
    print(f"Enviando os vetores para o dados PGVector: {pg_collection_name}")
    ids = [f"{Path(pdf_path).stem}-{i}" for i in range(len(enriched_docs))]
    vector_store.add_documents(documents=enriched_docs, ids=ids)

    print("--- Ingestão concluída com sucesso! ---")

if __name__ == "__main__":
    try:
        ingest_pdf()
    except Exception as e:
        print(f"Erro durante a ingestão do PDF {pdf_path}: {e}")