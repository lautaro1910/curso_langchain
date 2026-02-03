from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI

class AnalisisTexto(BaseModel):
    resumen: str = Field(description="Resumen breve del texto")
    sentimientos: list[str] = Field(description="Sentimiento del texto (Positivo, Negativo, Neutral)")
    
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.6)

structured_llm = llm.with_structured_output(AnalisisTexto)

texto = "Me encanta el fútbol, soy fanático de Liverpool."
print(structured_llm.invoke(f"Analiza el siguiente texto: {texto}").model_dump_json())



