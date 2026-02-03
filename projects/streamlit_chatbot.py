from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import PromptTemplate
import streamlit as st
import time

# Configurar la pagina de la app
st.set_page_config(page_title="Claudio Chatbot", page_icon="🤖")
st.title("🤖 Chatbot con LangChain")
st.markdown("Este es un chatbot que utiliza LangChain + streamlit para generar respuestas")

with st.sidebar:
    st.header("Configuración")
    st.selectbox("Modelo", options=["gemini-2.5-flash", "gemini-3.0-flash"], index=0)
    st.slider("Temperatura", min_value=0.0, max_value=1.0, value=0.5, step=0.1)
    chat_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.5)

# Inicializar el historial del chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Prompt base
prompt_template = PromptTemplate(
    input_variables=["message", "historial"],
    template="""
    Eres un asistente útil y muy amigable llamado Nicanor.
    Sos especialista en Marketing, SEO y Redes Sociales.
    Tu objetivo es ayudar a organizaciones a crecer y mejorar su presencia en línea.
    
    historial de conversación:
    {historial}
    
    Responde de manera clara y concisa a la siguiente pregunta del usuario:
    {message}
    """
)

# crear cadena usando LCEL (LangChain Expression Language)
chain = prompt_template | chat_model

# Mostrar mensajes previos en la interfaz
for message in st.session_state.messages:
    if isinstance(message, SystemMessage):
        # No muestro el mensaje del sistema
        continue

    role = "assistant" if isinstance (message, AIMessage) else "user"
    with st.chat_message(role):
        st.markdown(message.content)
    
# Input user
question = st.chat_input("¿En qué puedo ayudarte?")

if question:
    with st.chat_message("user"):
        st.markdown(question)
    
    try:
        # Mostrar la respuesta del chatbot
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""

            #streaming de la respuesta
            for chunk in chain.stream({
                "message": question,
                "historial": st.session_state.messages
            }):
                for char in chunk.content:
                    full_response += char
                    response_placeholder.markdown(full_response + "|")
                    time.sleep(0.005)
            response_placeholder.markdown(full_response)
        
        # Almacenamos el mensaje en la memoria de streamlit
        st.session_state.messages.append(HumanMessage(content=question))
        st.session_state.messages.append(AIMessage(content=full_response))
    except Exception as e:
        st.error(f"Error al generar respuesta: {str(e)}")

# Limpiar el chat
if st.button("Limpiar chat"):
    st.session_state.messages = []
    st.rerun()
