import os
from dotenv import load_dotenv
# from langchain_community.document_loaders import DirectoryLoader
# from langchain_community.vectorstores import InMemoryVectorStore
# from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langchain_classic.globals import set_debug
# from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore

# Debbuger
set_debug(True)


load_dotenv()
API_KEY_GROQ = os.getenv("API_KEY_GROQ")
MODEL_NAME_GROQ = os.getenv("MODEL_NAME_GROQ")
API_KEY_PINECONE = os.getenv('API_KEY_PINECONE')

# loader = DirectoryLoader("./Documentos/", glob="*.pdf")
# all_docs = loader.load()
# print(f'PDFs cargados: {len(all_docs)}')

# # Chunking semántico
# hf_embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-small")
# semantic_hf_splitter = SemanticChunker(hf_embeddings)
# semantic_hf_chunks = semantic_hf_splitter.split_documents(all_docs)
# print(f'Chunks: {len(semantic_hf_chunks)}')

# Vector Store
hf_embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-small")

vector_store = PineconeVectorStore(
    index_name="langchain-rag",
    embedding=hf_embeddings,
    pinecone_api_key=API_KEY_PINECONE
)

# vector_store.add_documents(semantic_hf_chunks)

retriver = vector_store.as_retriever(search_kwargs={'k': 3})

# Prompt
model = ChatGroq(api_key=API_KEY_GROQ, model='llama-3.3-70b-versatile')

prompt = ChatPromptTemplate(
    [
        ("system","Responde utilizando exclusivamente el contenido que se anexa a continuación: \nContexto:\n{contexto}"),
        ("human", "{query}")
    ]
)

rewriter_prompt_template = """
Genera la consulta de búsqueda para la base de datos de vectores (Vector DB) a partir de una pregunta del usuario,
permitiendo una respuesta más precisa por medio de la búsqueda semántica.
Basta devolver la consulta revisada del Vector DB, entre comillas.

# PREGUNTA DEL USUARIO: {user_question}
# CONSULTA REVISADA DEL VECTOR DB:
"""

rewriter_prompt = PromptTemplate.from_template(rewriter_prompt_template)
rewriter_chain = rewriter_prompt | model | StrOutputParser()

rag_chain = (
    {
        "contexto": RunnablePassthrough() | rewriter_chain | retriver,
        "query": RunnablePassthrough()
    } | prompt | model | StrOutputParser()
)

pregunta = "Cual es el propósito de la investigación?"

rag_chain.invoke(pregunta)
