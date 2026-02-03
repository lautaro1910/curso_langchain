from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st
import time

# Configurar la pagina de la app
st.set_page_config(page_title="Chatbot", page_icon="🤖")
st.title("🤖 Chatbot con LangChain")
st.markdown("Este es un chatbot que utiliza LangChain + streamlit para generar respuestas")

with st.sidebar:
    st.header("Configuración")
    st.selectbox("Modelo", options=["gemini-2.5-flash", "gemini-3.0-flash"], index=0)
    st.slider("Temperatura", min_value=0.0, max_value=1.0, value=0.5, step=0.1)
    chat_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.5)

    # Personalidad configurable
    personalidad = st.selectbox("Personalidad", options=["útil y muy amigable", "Profesional y formal", "Humorista", "Creativo y original", "Experto técnico"])

    system_messages = {
        "útil y muy amigable": "Eres un asistente útil y muy amigable llamado Nicanor. Responde de manera clara y concisa.",
        "Profesional y formal": "Eres un asistente profesional y formal llamado Juan. Responde de manera precisa y bien estructurado",
        "Humorista": "Eres un asistente humorista llamado Pedro. Responde de manera creativa y divertida",
        "Creativo y original": "Eres un asistente creativo y original llamado Ana. Responde de manera innovadora y creativa",
        "Experto técnico": "Eres un asistente experto técnico llamado Roger. Responde de manera precisa y bien estructurado"
    }

    # chat promptTemplate
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", system_messages[personalidad]),
        ("user", "Historial de conversación: {historial}\n\nResponde de manera clara y concisa a la siguiente pregunta del usuario: {message}")
    ])

    chain = chat_prompt | chat_model

# Inicializar el historial del chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes previos en la interfaz
for message in st.session_state.messages:
    if isinstance(message, SystemMessage):
        # No muestro el mensaje del sistema
        continue

    role = "assistant" if isinstance (message, AIMessage) else "user"
    with st.chat_message(role):
        st.markdown(message.content)

# Limpiar el chat
if st.button("Limpiar chat"):
    st.session_state.messages = []
    st.rerun()

    
# Input user
question = st.chat_input("¿En qué puedo ayudarte?")

if question:
    with st.chat_message("user"):
        st.markdown(question)
    
    # Prepara el historial como texto
    historial_text = ""
    for message in st.session_state.messages:
        if isinstance(message, HumanMessage):
            historial_text += f"Usuario: {message.content}\n"
        elif isinstance(message, AIMessage):
            historial_text += f"Asistente: {message.content}\n"

    if not historial_text:
        historial_text = "(No hay historial previo)"

    # Generar y mostrar rta
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

