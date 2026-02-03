from langchain_core.prompts import ChatPromptTemplate

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un traductor del español al inglés muy preciso."),
    ("user", "{text}")
])

print(chat_prompt.invoke({"text": "Zapatillas deportivas"}))

