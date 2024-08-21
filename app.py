import streamlit as st
from langchain_groq import ChatGroq
from sqlalchemy import create_engine
from langchain.agents.agent_types import AgentType
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities.sql_database import SQLDatabase
from langchain.callbacks import StreamlitCallbackHandler
from pathlib import Path
from langchain.agents import create_sql_agent
import sqlite3


LOCALDB="USE LOCALDB"
MYSQL="USE MYSQL"

st.set_page_config(page_title="LangChain: Chat with SQL DB", page_icon="🦜")
st.title("🦜 LangChain: Chat with SQL DB")
opt=["Use SQLLite 3 Database- Student.db","Connect to you MySQL Database"]
selected_option=st.sidebar.radio("Choose the DB which you want",options=opt)
if selected_option==opt[1]:
    db_uri=MYSQL
    mysql_host=st.sidebar.text_input("Enter host")
    mysql_user=st.sidebar.text_input("Enter user name")
    mysql_db=st.sidebar.text_input("Enter database")
    mysql_password=st.sidebar.text_input("Enter mysql password",type="password")
else:
    db_uri=LOCALDB

groq_api_key=st.sidebar.text_input("Enter groq api Key",type="password")

if not groq_api_key:
    st.info("Please enter Groq API key")
    st.stop()

llm=ChatGroq(groq_api_key=groq_api_key,model="Gemma2-9b-It")

if not db_uri:
    st.info("Please enter Databas information and db_uri")
def configure_db(db_uri,mysql_host=None,mysql_user=None,mysql_db=None,mysql_password=None):
    if db_uri==MYSQL:
        if not (mysql_host and mysql_user and mysql_db and mysql_password):
            st.error("enter SQL connection details")
            st.stop()
        return SQLDatabase(create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"))
    elif db_uri==LOCALDB:
        dbfilepath=(Path(__file__).parent/"student.db").absolute()
        creator=lambda:sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite:///",creator=creator))

if db_uri==MYSQL:
    db=configure_db(db_uri,mysql_host,mysql_user,mysql_db,mysql_password)
elif db_uri==LOCALDB:
    db=configure_db(db_uri)
    
toolkit=SQLDatabaseToolkit(db=db,llm=llm)

agent=create_sql_agent(
    toolkit=toolkit,
    verbose=False,
    llm=llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

if "messages" not in st.session_state or st.button("clear history"):
    st.session_state["messages"]=[{"role":"assistant","content":"Hi, i am a sql chatbot"}]
    
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg['content'])
    
user_query=st.chat_input(placeholder="ask anything about your Database")

if user_query:
    st.session_state.messages.append({"role":"user","content":user_query})
    st.chat_message("user").write(user_query)
    
    with st.chat_message("assistant"):
        callback_handler=StreamlitCallbackHandler(st.container())
        result=agent.run(user_query,callbacks=[callback_handler])
        st.session_state.messages.append({"role":"assistant","content":result})
        st.subheader(result)
    

        