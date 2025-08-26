import os

from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
os.environ["GOOGLE_API_KEY"] =os.getenv("GOOGLE_API_KEY") or ""

def CollectTheChartVariable(query:str , column_values , table):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    messages = [  
    ("system", "You are a experienced data analyst. you have to find out the X axis and Y axis key name for preparing a bar chart for the representation of the chart, Please Predict X and Y with Intelligence and with this info Typically, the x-axis has numbers for the time period or what is being measured, and the y-axis has numbers for the amount of stuff being measured. We will provide you the Column keys that are available in the data represtation with the data  along with the query of the user, you need to get the keys for X and Y axis , if it doesnt have any relation just responce with 'NO' , just responce with the value of the keys strictly don.t include anuy other informations."),  
    ("human", f" here the data table {table} here the columns present in the data {column_values} and here the human query {query}"),  
    ] 
    return str(llm.invoke(messages).content)
   