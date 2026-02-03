from langchain_core.messages import HumanMessage, SystemMessage, AIMessage


chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un traductor del español al inglés muy preciso."),
    ("user", "{question}")
    MessagePlaceholder(variable_name="historial", is_total_history=True)
])

# Simulamos un historial de conversacion
historial = [
    HumanMessage(content="Usuario: Cual es la capital de Francia?"),
    AIMessage(content="AI: La capital de Francia es París"),
    HumanMessage(content="Usuario: Cual es la capital de Italia?"),
    AIMessage(content="AI: La capital de Italia es Roma")
]

messages = chat_prompt.format_messages(
    {"historial": historial,
        "question": "¿Puedes decirme algo interesante de tu arquitectura?"})

for m in messages:
    print(m.content)