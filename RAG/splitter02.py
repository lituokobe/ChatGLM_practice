from langchain_text_splitters import RecursiveCharacterTextSplitter, HTMLHeaderTextSplitter

html_string = """
<!DOCTYPE html>
<html>
<body>
    <div>
        <h1>Foo</h1>

        <p>Some intro text about Foo.</p>
        <div>
            <h2>Bar main section</h2>
            <p>Some intro text about Bar.</p>
            <h3>Bar subsection 1</h3>
            <p>Some text about the first subtopic of Bar.</p>
            <h3>Bar subsection 2</h3>
            <p>Some text about the second subtopic of Bar.</p>
        </div>
        <div>
            <h2>Baz</h2>
            <p>Some text about Baz</p>
        </div>
        <br>
        <p>Some concluding text about Foo</p>
    </div>
</body>
</html>
"""
#html cutting
label_split = [ #define structure of the text
    ('h1', 'Chapter'),
    ('h2', 'Section'),
    ('h3', 'Point'),
    ('h4', 'Paragraph'),
]

html_splitter = HTMLHeaderTextSplitter(label_split)

docs = html_splitter.split_text(html_string)

docs2 = html_splitter.split_text_from_url('https://www.lituokobe.com/fight-against-misinformation-of-covid-19/')

print(docs2[0])
print('-------------------------')
print('There are ' + str(len(docs)) + ' chapters in total')
print('-------------------------')
print(docs2[1])

#as there are too many chapters ,we can cut twice
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=20,
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

docs_2_split = text_splitter.split_documents(docs2)
print('---------------------------')
print(len(docs_2_split))
print('---------------------------')
print(docs_2_split[4])
