# vscode
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(dotenv_path=find_dotenv(), override=True)

OPENAI_API_KEY:str|None=os.getenv(key="OPENAI_API_KEY")
PINECONE_API_KEY:str|None=os.getenv(key="PINECONE_API_KEY")
LANGCHAIN_API_KEY:str|None=os.getenv(key="LANGCHAIN_API_KEY")