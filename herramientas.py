import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langchain_pinecone import PineconeVectorStore

load_dotenv()
API_KEY_GROQ = os.getenv("API_KEY_GROQ")
MODEL_NAME_GROQ = os.getenv("MODEL_NAME_GROQ", "groq-1")
API_KEY_PINECONE = os.getenv('API_KEY_PINECONE')


def get_retriever():
    hf_embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-small")
    vector_store = PineconeVectorStore(
        index_name="alura-challenge",
        embedding=hf_embeddings,
        pinecone_api_key=API_KEY_PINECONE,
    )
    return vector_store.as_retriever(search_kwargs={"k": 3})

def get_model():
    return ChatGroq(api_key=API_KEY_GROQ, model_name=MODEL_NAME_GROQ, temperature=0)

def build_rag_chain(model, retriever):
    prompt = ChatPromptTemplate(
        [
            ("system","Responde utilizando exclusivamente el contenido que se anexa a continuación: \nContexto:\n{contexto}"),
            ("human", "{query}")
        ]
        )
    
    rewriter_prompt_template = """
                                Genera la consulta de búsqueda para la base de datos de vectores (Vector DB) a partir 
                                de una pregunta del usuario, permitiendo una respuesta más precisa por medio de la 
                                búsqueda semántica. Basta devolver la consulta revisada del Vector DB, entre comillas.

                                # PREGUNTA DEL USUARIO: {user_question}
                                # CONSULTA REVISADA DEL VECTOR DB:
                                """

    rewriter_prompt = PromptTemplate.from_template(rewriter_prompt_template)
    rewriter_chain = rewriter_prompt | model | StrOutputParser()

    return (
        {
            "contexto": RunnablePassthrough() | rewriter_chain | retriever,
            "query": RunnablePassthrough()
        } | prompt | model | StrOutputParser()
    )

def answer_pdf_question(query: str, rag_chain) -> str:   
    return rag_chain.invoke(query)

