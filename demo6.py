import os

from langchain.chains.sql_database.query import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
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
# print(db.dialect)
# print(db.get_usable_table_names())
# print(db.run("SELECT * FROM `world-politics_2`;"))# For MySQL

chain = create_sql_query_chain(llm = model, db=db)
#chain.get_prompts()[0].pretty_print()
"""
Below is the output of the line above, this means creating the #chain with create_sql_query_chain#,
by default there is already a prompt embedded for it to do some basic tasks:

'You are a MySQL expert. Given an input question, first create a syntactically correct MySQL query to run, then look at the results of the query and return the answer to the input question.
Unless the user specifies in the question a specific number of examples to obtain, query for at most 5 results using the LIMIT clause as per MySQL. You can order the results to return the most informative data in the database.
Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in backticks (`) to denote them as delimited identifiers.
Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
Pay attention to use CURDATE() function to get the current date, if the question involves "today".

Use the following format:
create_sql_query_chain
Question: Question here
SQLQuery: SQL Query to run
SQLResult: Result of the SQLQuery
Answer: Final answer here'
"""
resp = chain.invoke({'question':'which countries have expected live above 70'})
#print(resp)

sql = resp.replace('```sql', '').replace('```', '') #clean the format for SQL line
print(sql)

print(db.run(sql))
