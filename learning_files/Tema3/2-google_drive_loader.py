from langchain_google_community import GoogleDriveLoader

credentials_path = "learning_files/Tema3/credentials.json"
token_path = "learning_files/Tema3/token.json"

loader = GoogleDriveLoader(
    folder_id="1z6i2SqddX_UU1irBE2p9AvRL6tPMQW4L",
    credentials_path=credentials_path,
    token_path=token_path,
    recursive=True
)
documents = loader.load()

print(f"Metadata: {documents[0].metadata}")
print(f"Content: {documents[0].page_content}")

