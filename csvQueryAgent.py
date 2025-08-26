import os
from tabnanny import verbose
from langchain_community.utilities import SQLDatabase  
import pandas as pd
from sqlalchemy import create_engine
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain_experimental.sql.base import SQLDatabaseChain
from dotenv import load_dotenv
load_dotenv()

os.environ["GOOGLE_API_KEY"] =os.getenv("GOOGLE_API_KEY") or ""

engine = create_engine('sqlite:///database.db')
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
def CommunicateWithCSV(query : str , db):
    db_chain = SQLDatabaseChain.from_llm(llm , db , verbose=True)
    return db_chain(query)
