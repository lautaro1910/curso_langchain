from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

pregunta = "¿cuál fue la civilizacion maya?"
print("Pregunta: ", pregunta)

respuesta = llm.invoke(pregunta)
print("Respuesta: ", respuesta.content)

