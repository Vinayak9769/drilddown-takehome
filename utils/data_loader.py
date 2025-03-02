import json
from langchain_text_splitters import CharacterTextSplitter


def load_and_process_json(file_path):
    with open(file_path) as f:
        data = json.load(f)
    documents = []
    metadatas = []
    for item in data:
        description = item.get("general_description", "")
        sql = item.get("details") or item.get("query", "")
        documents.append(description)
        metadata = {
            "id": item.get("id"),
            "title": item.get("title", ""),
            "type": item.get("type", "report"),
            "sql": sql
        }
        metadatas.append(metadata)
    return documents, metadatas


def create_docs(file_path):
    documents, metadatas = load_and_process_json(file_path)
    text_splitter = CharacterTextSplitter(chunk_size=256, chunk_overlap=0)
    docs = text_splitter.create_documents(documents, metadatas=metadatas)
    return docs
