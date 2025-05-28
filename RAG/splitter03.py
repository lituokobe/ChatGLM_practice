from langchain_text_splitters import MarkdownHeaderTextSplitter


with open('Foo.md', encoding="utf-8") as f:
    text_data = f.read()

#makrdown cutting
label_split = [
    ('#', 'Chapter'),
    ('##', 'Section'),
    ('###', 'Point')
]

markdown_splitter = MarkdownHeaderTextSplitter(label_split, strip_headers=False)

docs = markdown_splitter.split_text(text_data)
print(docs)