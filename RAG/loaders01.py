from langchain_community.document_loaders import CSVLoader

#User LangChain to load CSV

loader = CSVLoader(file_path='../weather_district_id.csv', encoding='utf-8')

data = loader.load()

for record in data[:2]:
    print(record)