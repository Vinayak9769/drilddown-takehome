from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from chains.text_to_sql import create_text_to_sql_chain, print_all_documents_metadata
from chains.sql_executor import sql_executor_chain
from chains.pdf_generator import pdf_generation_chain
from utils.data_loader import create_docs
import argparse

data_file = "data/reports.json"
docs = create_docs(data_file)

embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
vectorstore = FAISS.from_documents(docs, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 1})

print_all_documents_metadata(vectorstore)

text_to_sql_chain = create_text_to_sql_chain(retriever)

final_chain = text_to_sql_chain | sql_executor_chain | pdf_generation_chain

def main():
    parser = argparse.ArgumentParser(description='Natural Language to SQL Report Generator')
    parser.add_argument('--query', type=str, required=False, help='Query in natural language')
    parser.add_argument('--output', type=str, default='sales_report.pdf', help='Output PDF filename')
    args = parser.parse_args()
    query = args.query if args.query else input("Enter your query: ")
    output_file = args.output
    final_output = final_chain.invoke(query)
    print(f"PDF generated: {final_output}")

if __name__ == "__main__":
    main()
