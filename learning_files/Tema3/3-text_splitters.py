from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import ChatGoogleGenerativeAI
# importar esta libreria para dividir el texto en chunks
from langchain.text_splitter import RecursiveCharacterTextSplitter

loader = PyPDFLoader("/home/lautaro/Downloads/resumen u6.pdf")
documents = loader.load()

# Dividir texto en chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=3000,
    chunk_overlap=200,
)

chuncks = text_splitter.split_documents(documents)

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)
summaries = []

for chunck in chuncks:
    response = llm.invoke(f"Haz un resumen de los puntos mas importantes del siguiente documento: {chunck}")
    summaries.append(response)

final_summary = llm.invoke(f"Combina y sintetiza estos resumenes en uno solo coherente y completo: {summaries}")
print(final_summary.content)
