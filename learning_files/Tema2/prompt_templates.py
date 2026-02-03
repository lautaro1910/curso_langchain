from langchain_core.prompts import PromptTemplate

template = "Eres un experto en marketing, SEO y Redes Sociales. Sugiere un slogan creativo para un producto {product}. El slogan debe ser corto, pegadizo y fácil de recordar."

prompt = PromptTemplate(template=template, input_variables=["product"])

print(prompt.format(product="Zapatillas deportivas"))