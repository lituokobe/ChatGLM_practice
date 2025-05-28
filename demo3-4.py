import os

from langchain_chroma import Chroma
from langchain_community.embeddings import ModelScopeEmbeddings
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI

api_key = os.getenv('GLM_API_KEY')
os.environ['LANGCHAIN_TRACING'] = "true"
os.environ['LANGSMITH_ENDPOINT'] = "https://api.smith.langchain.com"
os.environ['LANGSMITH_PROJECT'] = "pr-shadowy-maybe-22"
os.environ['LANGCHAIN_PROJECT'] = "Tuo-Demo"

model = ChatOpenAI(model = 'glm-4-0520',
                   api_key= api_key,
                   base_url='https://open.bigmodel.cn/api/paas/v4/',
                   temperature= 0.6)

documents = [
    Document(
        page_content="狗是伟大的伴侣，以其忠诚和友好而闻名。",
        metadata={"source": "哺乳动物宠物文档"},
    ),
    Document(
        page_content="猫是独立的宠物，通常喜欢自己的空间。",
        metadata={"source": "哺乳动物宠物文档"},
    ),
    Document(
        page_content="金鱼是初学者的流行宠物，需要相对简单的护理。",
        metadata={"source": "鱼类宠物文档"},
    ),
    Document(
        page_content="鹦鹉是聪明的鸟类，能够模仿人类的语言。",
        metadata={"source": "鸟类宠物文档"},
    ),
    Document(
        page_content="兔子是社交动物，需要足够的空间跳跃。",
        metadata={"source": "哺乳动物宠物文档"},
    ),
]

#Use GTE embeddings from ModelScope, no VPN required in China
embeddings = ModelScopeEmbeddings (model_id = 'iic/nlp_gte_sentence-embedding_chinese-base')

vector_store = Chroma.from_documents(documents, embedding =embeddings)

print(vector_store.similarity_search_with_score('咖啡猫'))

