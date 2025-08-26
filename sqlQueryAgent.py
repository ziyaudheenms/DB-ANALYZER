import os
from tabnanny import verbose
from  langchain_community.utilities import SQLDatabase
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_experimental.sql.base import SQLDatabaseChain

load_dotenv()

os.environ["GOOGLE_API_KEY"] =os.getenv("GOOGLE_API_KEY") or ""
# db_uri = f"postgresql+psycopg2://IdeaWall_owner:npg_SoYZflx4NPL0@ep-tight-sea-a9voobr9-pooler.gwc.azure.neon.tech/IdeaWall?sslmode=require&channel_binding=require"
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

def ExecuteSQL(query : str , db):
    # db = SQLDatabase.from_uri(db_URL)
    # print(db.table_info)
        
    messages = [  
        ("system", f"You are a helpfull agent and your duty is to analyse the user query that is to be converted into sql and check whether the query is related to the information of the sql database {db.table_info} , if it has no relation just responce with NO and if has relation just responce with YES."),  
        ("human", f"here the information about the database : {query}"),  
    ]
    flag = llm.invoke(messages).content

    if flag == "YES" or flag == "yes":
        db_chain = SQLDatabaseChain.from_llm(llm , db , verbose = True)
        sql_res =  db_chain(query)["result"]
        res = llm.invoke(f"just give the sql commands from {sql_res} to fetch the data , please include only the sql command don't add anything extra")
        print(res.content)
        str_sql = str(res.content)
        str_sql = str_sql.replace("```sql", "").replace("```", "").strip()
        responce = db.run(str_sql)
        print("responce")
        return {
            "answer" : responce,
            "sql_command" : str_sql
        }
    else:
        return {
            "answer" : "Sorry The Query is not related to the database",
            "sql_command" : ""
        }

