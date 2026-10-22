from langchain_community.tools import DuckDuckGoSearchResults
from nevara.globalOp import document_retriever
from langchain_core.tools import tool
import os

@tool
def retrieve_document(query: str):
    """
        If any file that user have uploaded, You can see through this tool.
        use query parameter to find document what you are looking for.
    """
    retriever = document_retriever.get_retriever()
    matching_docs = retriever.invoke(query)

    data = ""
    for doc in matching_docs:
        file_path = doc.metadata.get("source", "unknown source")
        file_name = os.path.basename(file_path)
        file_content = doc.page_content
        data += f"file: {file_name}\n{file_content}\n"

    return data or "No Document provided by user yet."

ddgs_results = DuckDuckGoSearchResults()
sacred_tools = [retrieve_document, ddgs_results]