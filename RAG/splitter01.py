from langchain_text_splitters import RecursiveCharacterTextSplitter

with open('test.txt', encoding="utf-8") as f:
    text_data = f.read()

#recursive cutting
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20, #maximus overlapped between chunks
    length_function=len, #use count of the len as the function
    is_separator_regex=False, #No regrex
    separators=['\n\n', '\n', '.', '?', '!',
                ',',' '] #define the separators with PRIORITY
)

# chunks_list = text_splitter.split_documents([text_data])
chunks_list = text_splitter.create_documents([text_data])
print(len(chunks_list))
print(chunks_list[0])
print(chunks_list[1])