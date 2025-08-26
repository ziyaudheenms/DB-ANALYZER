import os
import re
import pandas as pd
import streamlit as st

from langchain_community.utilities import SQLDatabase
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from io import BytesIO

from sqlQueryAgent import ExecuteSQL
from Output_Refinment import RefineTheAgentResponce
from csvQueryAgent import CommunicateWithCSV
from sqlalchemy import create_engine
from Column_Analyzer import CollectTheChartVariable
os.environ["GOOGLE_API_KEY"] =os.getenv("GOOGLE_API_KEY") or ""
st.markdown(
    """
    <h1 style="text-align:center; color:#4F8BF9; font-size: 3em; margin-bottom: 0.2em;">
        🚀 Welcome to <span style="color:#F97C4F;">DBAnalyzer</span>!
    </h1>
   
    """,
    unsafe_allow_html=True
)
import time


if "queries" not in st.session_state:
    st.session_state.queries = []

if "answers" not in st.session_state:
    st.session_state.answers = []

if "sql_commands" not in st.session_state:
    st.session_state.sql_commands = []

if "sql" not in st.session_state:
    st.session_state.sql = False

if "csv" not in st.session_state:
    st.session_state.csv = False

if "db_loaded" not in st.session_state:
    st.session_state.db_loaded = False
    st.session_state.sql_db = None

with st.sidebar:
    st.header("LOAD YOUR DATABASE WITH US")
    st.write("Select The Type Of The Database To Communicate !")
    sql, csv = st.columns(2)
    with sql:
        sql = st.button("SQL DB", use_container_width=True)
    with csv:
        csv = st.button("CSV FILE",use_container_width=True)
    if sql:
        st.session_state.sql = True
    if csv:
        st.session_state.csv = True

    if st.session_state.sql:
        st.text_input("Paste the connection string of db", key="POSTGRESQL_CONNECTION_STRING",icon="✍️")
        if st.session_state.POSTGRESQL_CONNECTION_STRING and not st.session_state.db_loaded:
            with st.spinner("🤖 Loading the Database ..."):
                try:
                    st.session_state.sql_db = SQLDatabase.from_uri(f"postgresql+psycopg2://{st.session_state.POSTGRESQL_CONNECTION_STRING}")
                    st.session_state.db_loaded = True
                    st.success("Database connected successfully!")
                except Exception as e:
                    st.error(f"Failed to connect to the database: {e}")
                    st.session_state.db_loaded = False
    
    if st.session_state.csv:
        uploaded_file = st.file_uploader("Choose a file")

        if uploaded_file is not None:
           with st.spinner("🤖 Loading the Database ...") :
                bytes_data = uploaded_file.getvalue()
                bytes_io = BytesIO(bytes_data)
                df = pd.read_csv(bytes_io)
                st.write(df)
                print(df.columns)
                st.session_state.column = df.columns
                st.session_state.csv_df = df
                engine = create_engine('sqlite:///database.db')
                df.to_sql("Database" , engine , index=False , if_exists="replace")
                st.session_state.sql_db = SQLDatabase(engine=engine)
                st.success("Database connected successfully!")
                
        if st.button("Generate Analysis Report",use_container_width=True):
            with st.spinner("🤖 Generating Report ..."):
                report = CommunicateWithCSV("Analyse The DataBase Given To You and Prepare a detailed and amazing informatice insights of the database." , st.session_state.sql_db)
                st.write(report["result"])
                downloadable_data = report["result"].encode('utf-8')
                st.download_button("Download Report", data=downloadable_data, file_name="analysis_report.txt")


user_query = st.chat_input("Ask a question about your database:")

if user_query:
    st.session_state.queries.append(user_query)
    if st.session_state.sql_db:
        if st.session_state.sql:

            result = ExecuteSQL(user_query, st.session_state.sql_db)
            st.session_state.sql_commands.append(result["sql_command"])
            refined_answer = RefineTheAgentResponce(user_query , str(result))
            st.session_state.answers.append(refined_answer)
        elif st.session_state.csv:
            charts_val = CollectTheChartVariable(user_query,st.session_state.column , st.session_state.csv_df)
            if charts_val != "NO" and charts_val != "no":
                st.session_state.sql_commands.append(charts_val)
            result = CommunicateWithCSV(user_query , st.session_state.sql_db)
            print(result)
            st.session_state.answers.append(result['result'])

def write_stream(content):
    st.write(content)

for i in range(len(st.session_state.queries)):
    st.markdown(
        f"""
        <div style="
            display: flex;
            justify-content: flex-end;
            width: 100%;
        ">
            <div style="
                background-color: black;
                min-width: 100px;
                max-width: 60%;
                border-radius: 12px;
                padding-top: 10px;
                padding-bottom: 10px;
                padding-right: 16px;
                padding-left: 16px;
                margin-bottom: 10px;
                border: 1px solid #0E1117;
                box-shadow: 0 2px 8px rgba(0,0,0,0.04);
                text-align: left;
                ">
                <span style="font-size: 22px; color: white;"> <b></b> {st.session_state.queries[i]}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if i < len(st.session_state.sql_commands):
        if st.session_state.sql:

            with st.expander("SQL Command that is being executed"):
                st.code(st.session_state.sql_commands[i], language="sql")
        elif st.session_state.csv:
            print(st.session_state.sql_commands[i])
            X,Y= st.session_state.sql_commands[i].split("\n")
            if X == "Survived":
            
                with st.expander("CSV Data that is being processed"):
                    st.bar_chart(st.session_state.csv_df , x=Y, y=X)
            else:
                with st.expander("CSV Data that is being processed"):
                    st.bar_chart(st.session_state.csv_df , x=X, y=Y)

    if i < len(st.session_state.answers):
        st.markdown(
            f"""
            <div style="
                display: flex;
                justify-content: flex-start;
                width: 100%;
            ">
                <div style="
                    min-width: 100px;
                    max-width: 90%;
                    border-radius: 12px;
                    padding-top: 10px;
                    padding-bottom: 10px;
                    padding-right: 16px;
                    padding-left: 16px;
                    margin-bottom: 2px;
                    border: 1px solid #0E1117;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
                    text-align: left;
                    ">
                    <span style="font-size: 22px; color: white; display:flex; align-items:center; gap:8px;"> <b style = "font-size: 50px;">🤖 </b> {st.session_state.answers[i]}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

with st.sidebar:
    if st.session_state.db_loaded:
        st.title("DETAILS OF THE DATABASE")
        st.header("Tables in the Database")
        for table in st.session_state.sql_db.get_usable_table_names():
            pattern = re.compile(r'^\s*([a-zA-Z_]\w*)\s.*?(?:,|$)', re.MULTILINE)
            column_names = [match.group(1) for match in pattern.finditer(st.session_state.sql_db.get_table_info([table])) if not match.group(0).strip().upper().startswith(("CONSTRAINT", "PRIMARY KEY", "FOREIGN KEY"))]
            new_column_list = [item for item in column_names if item != 'CREATE']
            unique_list = list(set(new_column_list))
            # Add a unique key to each selectbox
            st.selectbox(label=table, options=unique_list, key=table)