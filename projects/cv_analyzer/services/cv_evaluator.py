from langchain_google_genai import ChatGoogleGenerativeAI
from models.cv_model import AnalyzeCV
from prompts.cv_prompts import crear_sistema_prompts
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import google.api_core.exceptions

def crear_evaluador():
    modelo_base = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        temperature=0.2
    )

    modelo_estructurado = modelo_base.with_structured_output(AnalyzeCV)
    chat_prompt = crear_sistema_prompts()
    chain_evaluation = chat_prompt | modelo_estructurado

    return chain_evaluation

# Configuración de reintentos: 
# Espera exponencial (2s, 4s, 8s...) hasta 5 intentos
# Solo reintenta si el error es ResourceExhausted (429)
@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=4, max=60),
    retry=retry_if_exception_type(google.api_core.exceptions.ResourceExhausted)
)
def ejecutar_con_reintentos(chain, inputs):
    return chain.invoke(inputs)

def evaluar_candidato(cv_text: str, job_description: str) -> AnalyzeCV:
    try:
        chain_evaluation = crear_evaluador()
        
        # Usamos la función con reintentos
        result = ejecutar_con_reintentos(chain_evaluation, {
            "descripcion_puesto": job_description,
            "texto_cv": cv_text
        })
        return result
        
    except Exception as e:
        print(f"Error crítico al evaluar el CV después de reintentos: {e}")
        error_msg = str(e)
        if "429" in error_msg or "ResourceExhausted" in error_msg:
             error_msg = "⚠️ El sistema está saturado (Límite de cuota gratuito). Intenta de nuevo en unos minutos."
        
        return AnalyzeCV(
            name_candidate="Error de Procesamiento",
            years_of_experience=0,
            abilities=[error_msg],
            education=["Error en análisis"],
            experience=["No se pudo procesar el análisis debido a un error en el servicio."],
            strengths=["Intenta nuevamente más tarde"],
            areas_for_improvement=[],
            percentage_match=0
        )