from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

template = PromptTemplate(
    input_variables=["nombre"],
    template="""
    Saluda a {nombre} de manera amable.
    Y preséntate.
    """
)

# Usando el operador pipe (|) en lugar del deprecated LLMChain
chain = template | llm

result = chain.invoke({"nombre": "Lautaro"})
print(result.content)



