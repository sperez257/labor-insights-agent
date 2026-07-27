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
        # .stApp {background-color: #f8f9fb;}
        .title {font-size: 2.25rem; font-weight: 700; color: #0f172a;}
        .subtitle {color: #475569; margin-bottom: 1rem;}
        .stTextArea>div>div>textarea {font-size: 1rem;}
        # .stButton>button {background-color: #0f172a; color: white;}
        .sidebar-heading {font-size: 1rem; font-weight: 700; margin-bottom: 0.75rem;}
        .sidebar-text {margin-bottom: 0.75rem; line-height: 1.4;}
        .sidebar-tag-group {display: flex; flex-wrap: wrap; gap: 0.4rem;}
        .sidebar-tag {display: inline-flex; align-items: center; justify-content: center; padding: 0.45rem 0.75rem; border-radius: 999px; font-size: 0.9rem; background: #f8fafc; border: 1px solid #e2e8f0; color: #0f172a;}
        .sidebar-tag-green {background-color: #ecfdf5; border-color: #22c55e;}
        .sidebar-tag-yellow {background-color: #fef3c7; border-color: #f59e0b;}
        .sidebar-card {border: 1px solid #e2e8f0; border-radius: 1rem; padding: 0.9rem 1rem; margin-bottom: 0.75rem; box-shadow: 0 8px 20px rgba(15, 23, 42, 0.04);}
        .sidebar-card-title {font-size: 0.96rem; font-weight: 700; margin-bottom: 0.35rem;}
        .sidebar-card-text {font-size: 0.9rem; line-height: 1.5;}
    </style>
    """,
    unsafe_allow_html=True,
)

def main():
    st.title("Labor Insights Agent")
    st.markdown("##### Inteligencia y análisis del mercado laboral peruano")
    st.markdown("Explora información de la Encuesta Permanente de Empleo Nacional (EPEN), consulta documentos metodológicos y analiza datos del mercado laboral para obtener insights claros y fundamentados.")
    # st.markdown("EPEN · Perú · Trimestre I 2026")
    

    with st.sidebar:
        st.markdown("<div class='sidebar-section'>", unsafe_allow_html=True)
        st.markdown("<div class='sidebar-heading'>Fuente de información</div>", unsafe_allow_html=True)
        st.markdown("<div class='sidebar-card'><div class='sidebar-card-title'>Encuesta Permanente de Empleo Nacional (EPEN)</div><div class='sidebar-card-text'>Perú · Trimestre I 2026</div></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='sidebar-section'>", unsafe_allow_html=True)
        # st.markdown("<div class='sidebar-heading'>Base de conocimiento</div>", unsafe_allow_html=True)
        # st.markdown(
        #     "<div class='sidebar-tag-group'>"
        #     "<span class='sidebar-tag sidebar-tag-green'>Diccionario de datos</span>"
        #     "<span class='sidebar-tag sidebar-tag-green'>Ficha técnica</span>"
        #     "<span class='sidebar-tag sidebar-tag-green'>Informe técnico</span>"
        #     "<span class='sidebar-tag sidebar-tag-yellow'>Datos CSV (Próximamente)</span>"
        #     "</div>",
        #     unsafe_allow_html=True,
        # )
        # st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='sidebar-heading'>¿Qué puedo hacer?</div>", unsafe_allow_html=True)
        st.markdown(
            "<div class='sidebar-card'><div class='sidebar-card-title'>📚 Consultar documentación</div><div class='sidebar-card-text'>Responde preguntas sobre metodología, variables y conceptos.</div></div>"
            "<div class='sidebar-card'><div class='sidebar-card-title'>📊 Analizar indicadores</div><div class='sidebar-card-text'>Interpreta métricas y resultados disponibles.</div></div>"
            "<div class='sidebar-card'><div class='sidebar-card-title'>🏙️ Comparar ciudades</div><div class='sidebar-card-text'>Identifica diferencias entre ciudades investigadas.</div></div>"
            "<div class='sidebar-card'><div class='sidebar-card-title'>🔍 Generar insights</div><div class='sidebar-card-text'>Resume tendencias y patrones encontrados en los datos.</div></div>",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    question = st.text_area(label="¿Qué quieres investigar?", placeholder="Pregunta sobre empleo, desempleo, ingresos o ciudades.")

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
