from langchain_core.runnables import RunnableLambda, RunnableParallel
from langchain_google_genai import ChatGoogleGenerativeAI
import json

# config del modelo
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

def preprocess_text(text):
    return text.strip()[:500]
 
# Convertir la función en un Runnable
preprocessor = RunnableLambda(preprocess_text)

# Generar resumen
def generate_summary(text):
    prompt = f"Resume en una sola oración el siguiente texto: {text}. Es importante que seas directo y breve."
    response = llm.invoke(prompt)
    return response.content

# Analisis de sentimiento
def analyze_sentiment(text):
    prompt = f"""Analiza el sentimiento del siguiente texto.
    Responde ÚNICAMENTE en formato JSON válido:
    {{"sentimiento": "positivo|negativo|neutro", "razon": "justificación breve"}}
    
    Texto: {text}"""
    
    response = llm.invoke(prompt)
    content = response.content.strip()
    if content.startswith("```json"):
        content = content[7:-3].strip()
    elif content.startswith("```"):
        content = content[3:-3].strip()
        
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {"sentimiento": "NO DATA", "razon": "Error en análisis"}

# Combinar resultados
def merge_results(data):
    return {
        "resumen": data["resumen"],
        "sentimiento": data["sentimiento_data"]["sentimiento"],
        "razon": data["sentimiento_data"]["razon"]
    }

summary_branch = RunnableLambda(generate_summary)
sentiment_branch = RunnableLambda(analyze_sentiment)
merge_branch = RunnableLambda(merge_results)

parallel_tasks = RunnableParallel({
    "resumen": summary_branch,
    "sentimiento_data": sentiment_branch
})

chain = preprocessor | parallel_tasks | merge_branch

# Test
review_batch = [
    """
    ¡Hola! Quería contarles que estoy muy feliz con el producto. 
    Llegó en perfecto estado y funciona de maravilla. 
    La calidad es excelente y superó mis expectativas. 
    Definitivamente lo recomendaría a mis amigos.
    """,
    """
    El producto llegó en mal estado y no funciona correctamente. 
    Estoy muy decepcionado con la compra.
    """,
    """
    El producto es bueno y cumple con lo prometido. 
    No tengo quejas.
    """
]

result = chain.batch(review_batch)
print(result)