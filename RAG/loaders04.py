from langchain_community.document_loaders import UnstructuredMarkdownLoader

#entire md in one document
# loader = UnstructuredMarkdownLoader(file_path="test_translated.md")

loader = UnstructuredMarkdownLoader(file_path="test_translated.md", model = 'elements')

data = loader.load()

print(data)