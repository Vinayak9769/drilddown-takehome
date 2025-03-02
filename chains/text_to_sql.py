from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_ollama import OllamaLLM
from utils.json_parser import json_output_parser
import json

def debug_context(inputs):
    print("\n" + "="*50)
    print("RETRIEVED CONTEXT:")
    if isinstance(inputs["context"], list):
        for i, doc in enumerate(inputs["context"]):
            print(f"\nDocument {i+1}:")
            print(f"Content: {doc.page_content}")
            print(f"Metadata: {json.dumps(doc.metadata, indent=2)}")
    else:
        print(f"Context: {inputs['context']}")
    print("\nQuery: " + inputs["question"])
    print("="*50 + "\n")
    return inputs

def print_all_documents_metadata(vectorstore):
    """
    Utility function to print metadata for all documents in the vectorstore
    
    Args:
        vectorstore: FAISS vectorstore containing the documents
    """
    print("\n" + "="*50)
    print("ALL DOCUMENTS IN VECTORSTORE:")
    print("="*50)
    
    docs = vectorstore.similarity_search("", k=1000)
    
    for i, doc in enumerate(docs):
        print(f"\nDocument {i+1}:")
        print(f"Content Preview: {doc.page_content[:150]}..." if len(doc.page_content) > 150 else doc.page_content)
        print(f"Metadata: {json.dumps(doc.metadata, indent=2)}")
    
    print(f"\nTotal Documents: {len(docs)}")
    print("="*50 + "\n")

prompt_template = """You are a SQL expert analyzing sales data. Follow these steps:
1. Look at the context provided below.
2. Identify the SQL query that answers the query.
3. Based on the query and context, determine an appropriate, short report title.
4. Return your result as a JSON object with two keys: "title" and "sql". 
   - The "sql" field must contain only the exact SQL query in quotations.
   - The "title" field should be a short descriptive title for the report.
5. STRICTLY RETURN JUST THE JSON NO COMMENTARY
6. DO NOT WRITE YOUR OWN SQL QUERY AT ANY COST, IT MUST BE FROM THE PROVIDED CONTEXT

Context:
{context}

Query: {question}
"""

def create_text_to_sql_chain(retriever):
    prompt = ChatPromptTemplate.from_template(prompt_template)
    
    llm = OllamaLLM(model="llama3.2", temperature=0.1)
    
    text_to_sql_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | RunnableLambda(debug_context) 
        | prompt
        | llm
        | RunnableLambda(func=json_output_parser)
    )
    
    return text_to_sql_chain
