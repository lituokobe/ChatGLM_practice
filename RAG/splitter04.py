import os

from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import MarkdownHeaderTextSplitter

os.environ['LANGCHAIN_TRACING'] = "true"
os.environ['LANGSMITH_ENDPOINT'] = "https://api.smith.langchain.com"
os.environ['LANGSMITH_PROJECT'] = "pr-shadowy-maybe-22"
os.environ['LANGCHAIN_PROJECT'] = "Tuo-Demo"

#semantic cutting
with open('test.txt', encoding="utf-8") as f:
    text_data = f.read()

# Initialize with the specific embedding model
embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small")

text_splitter = SemanticChunker(embeddings_model,
                                breakpoint_threshold_type='percentile') #Use percentile method to cut
docs_list = text_splitter.create_documents([text_data])

print(docs_list[0].page_content)