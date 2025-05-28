import os
from operator import itemgetter

from langchain.chains.sql_database.query import create_sql_query_chain
from langchain_community.tools import QuerySQLDataBaseTool
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

api_key = os.getenv('GLM_API_KEY')
os.environ['LANGCHAIN_TRACING'] = "true"
os.environ['LANGSMITH_ENDPOINT'] = "https://api.smith.langchain.com"
os.environ['LANGSMITH_PROJECT'] = "pr-shadowy-maybe-22"
os.environ['LANGCHAIN_PROJECT'] = "Tuo-Demo"

#set up the database info
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'world_bank_data'
USERNAME = 'root'
PASSWORD = ''
MYSQL_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)

# Create the model
model = ChatOpenAI(
    model='glm-4-0520',
    api_key=api_key,
    base_url='https://open.bigmodel.cn/api/paas/v4/',
    temperature=0.6
)

#create the database
db = SQLDatabase.from_uri(MYSQL_URI)

create_sql = create_sql_query_chain(llm = model, db=db)

create_sql = create_sql | (lambda x:x.replace('```sql', '').replace('```', '') )

execute_sql = QuerySQLDataBaseTool(db = db) #LangChain's internal tool

answer_prompt = PromptTemplate.from_template(
    """
    Give the the following question, corresponding SQL query, and SQL result, answer the question in Spanish.
    question: {question}
    SQL Query: {query}
    SQL Result: {result}
    Answer:
    """
)

answer_chain = answer_prompt | model | StrOutputParser()

chain = RunnablePassthrough.assign(query = create_sql).assign(result = itemgetter('query') | execute_sql) | answer_chain

resp = chain.invoke({'question':'which countries have expected live above 70? What are their GDP per capita?'})

print(resp)
