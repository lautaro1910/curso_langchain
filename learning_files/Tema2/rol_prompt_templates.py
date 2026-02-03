from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

plantilla_sistema = SystemMessagePromptTemplate.from_template(
    "Eres un {rol} especializado en {especialidad}. Responde de manera {tono}."
)

plantilla_usuario = HumanMessagePromptTemplate.from_template(
    "Mi pregunta sobre {tema} es: {pregunta}"
)

chat_prompt = ChatPromptTemplate.from_messages([
    plantilla_sistema,
    plantilla_usuario
])

print(chat_prompt.invoke({
    "rol": "nutricionista",
    "especialidad": "alimentación saludable",
    "tono": "amigable",
    "tema": "proteinas vegetales para entrenar",
    "pregunta": "¿Cuales son las mejores proteinas vegetales para entrenar musculación?"
}))

for m in chat_prompt.invoke({
    "rol": "nutricionista",
    "especialidad": "alimentación saludable",
    "tono": "amigable",
    "tema": "proteinas vegetales para entrenar",
    "pregunta": "¿Cuales son las mejores proteinas vegetales para entrenar musculación?"
}):
    print(m.content)