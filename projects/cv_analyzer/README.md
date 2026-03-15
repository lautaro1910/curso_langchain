# CV Analyzer

El **CV Analyzer** es una aplicación desarrollada en Python con Streamlit que utiliza inteligencia artificial (Google Gemini) para evaluar la idoneidad de un candidato para un puesto de trabajo específico.

## Características

- Carga de CV en formato PDF.
- Análisis comparativo con descripción del puesto.
- Evaluación detallada de años de experiencia, habilidades, educación, y fortalezas.
- Sugerencias de mejora.
- Porcentaje de coincidencia (Match).

## Requisitos Previos

Necesitas tener instalado Python 3.10 o superior.

Las librerías principales que utiliza el proyecto son:

- `streamlit`
- `langchain-google-genai`
- `langchain`
- `python-dotenv`
- `pypdf` (para leer PDFs)

## Instalación

1.  Clona el repositorio o navega hasta la carpeta del proyecto:

    ```bash
    cd projects/cv_analyzer
    ```

2.  Activa tu entorno virtual (si no lo has hecho):

    ```bash
    source ../../venv/bin/activate
    ```

3.  Instala las dependencias necesarias:
    ```bash
    pip install streamlit langchain-google-genai python-dotenv pypdf
    ```

## Configuración

El proyecto requiere una **API Key de Google Gemini**.

1.  Crea un archivo `.env` en la raíz del proyecto (o asegúrate de que tus variables de entorno estén cargadas).
2.  Agrega tu clave:
    ```env
    GOOGLE_API_KEY=tu_api_key_aqui
    ```

## Uso

Para ejecutar la aplicación, utiliza el siguiente comando desde la terminal:

```bash
streamlit run app.py
```

Esto abrirá una pestaña en tu navegador (usualmente en `http://localhost:8501`) donde podrás:

1.  Pegar la descripción del puesto de trabajo.
2.  Subir el archivo PDF del CV del candidato.
3.  Hacer clic en "Analizar CV" para ver los resultados.

## Estructura del Proyecto

- `app.py`: Punto de entrada de la aplicación.
- `ui/`: Contiene la lógica de la interfaz de usuario.
- `services/`: Lógica de negocio y conexión con la IA.
- `prompts/`: Definición de los prompts utilizados para el análisis.
- `models/`: Definición de los modelos de datos (estructuras de salida).
