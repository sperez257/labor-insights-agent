import streamlit as st
from herramientas import get_model, get_retriever, answer_pdf_question, build_rag_chain

@st.cache_resource
def cached_model():
    return get_model()

@st.cache_resource
def cached_retriever():
    return get_retriever()

@st.cache_resource
def cached_rag_chain():
    model = get_model()
    retriever = get_retriever()

    return build_rag_chain(
        model,
        retriever
    )

st.set_page_config(page_title="Herramienta IA Empleo Perú", layout="wide")

st.markdown(
    """
    <style>
        .stApp {background-color: #f8f9fb;}
        .title {font-size: 2.25rem; font-weight: 700; color: #0f172a;}
        .subtitle {color: #475569; margin-bottom: 1rem;}
        .stTextArea>div>div>textarea {font-size: 1rem;}
        .stButton>button {background-color: #0f172a; color: white;}
    </style>
    """,
    unsafe_allow_html=True,
)

def main():
    st.title("Herramienta RAG de Empleo Perú")
    st.markdown("Una interfaz minimalista para hacer preguntas a los documentos PDF indexados en Pinecone.")

    with st.sidebar:
        st.header("Guía rápida")
        st.markdown("- Pregunta sobre los documentos de empleo en Perú.")
        st.markdown("- El agente usa solo la base de conocimiento RAG en Pinecone.")
        st.markdown("- Evita consultas relacionadas con archivos CSV en esta versión.")
        st.markdown("---")
        st.markdown("### Objetivo")
        st.markdown("Investigar tendencias, políticas y datos de empleo con respuestas claras y enfocadas.")

    question = st.text_area("Escribe tu pregunta", height=180)

    if st.button("Consultar agente"):
        if not question.strip():
            st.warning("Por favor ingresa una pregunta antes de enviar.")
            return

        with st.spinner("Consultando la base de conocimiento RAG..."):
            answer = answer_pdf_question(question, cached_rag_chain())

        st.markdown("### Respuesta del agente")
        st.write(answer)

    st.markdown("---")
    st.markdown("Hecho para investigadores y analistas que desean una experiencia limpia y sin distracciones.")


if __name__ == "__main__":
    main()
