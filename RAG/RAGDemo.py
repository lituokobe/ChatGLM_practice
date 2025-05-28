import os
from langchain.vectorstores import lancedb
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import LanceDB
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from ChatGLM_practice.RAG.splitter01 import text_splitter

os.environ['LANGCHAIN_TRACING'] = "true"
os.environ['LANGSMITH_ENDPOINT'] = "https://api.smith.langchain.com"
os.environ['LANGSMITH_PROJECT'] = "pr-shadowy-maybe-22"
os.environ['LANGCHAIN_PROJECT'] = "Tuo-Demo"
api_key = os.getenv('GLM_API_KEY')

print('good')

loader = TextLoader('chinese_news.txt', encoding='utf-8')
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=0,
    length_function=len,
    is_separator_regex=False,
    separators=[
        "\n\n",
        "\n",
        ".",
        "?",
        "!",
        "。",
        "！",
        "？",
        ",",
        "，",
        " "
    ]
)

docs = text_splitter.split_documents(documents)
print('===================', len(docs))
embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small")

#connect to a local vector database
db_path = os.path.join(os.getcwd(), 'lanceDB')
connection = lancedb.connect(db_path)

vectorStore = LanceDB.from_documents(docs, embeddings_model, connection = connection, table_name = 'news_vetors')

query = '今年长三角铁路春游运输共经历多少天？'
#
# docs_and_score = vectorStore.similarity_search_with_score(query)
#
# for doc, score in docs_and_score:
#     print('--------------------')
#     print('Score: ', score)
#     print('Content: ', doc.page_content)

# integrate it with LLM
retriever = vectorStore.as_retriever()
template = """Answer the question based only on the following context:
{context}
Question: {question}
"""

prompt = ChatPromptTemplate.from_template(template)

# create model
model = ChatOpenAI(
    model='glm-4-0520',
    api_key=api_key,
    base_url='https://open.bigmodel.cn/api/paas/v4/'
)

output_parser = StrOutputParser()

#  combine the retriever and user question
start_retriever = RunnableParallel({'context': retriever, 'question': RunnablePassthrough()})

# Create a chain
chain = start_retriever | prompt | model | output_parser

res = chain.invoke(query)
print(res)
