#User LangChain to load HTML
import bs4
from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader(
    web_path=('https://www.lituokobe.com/challenges-in-digital-transformation-for-large-enterprises/',),
    encoding='utf-8',
    bs_kwargs=dict(parse_only = bs4.SoupStrainer(class_=('blog-content'))) #only get the content in class blog-content of the webpage
)

docs = loader.load()
print(docs)