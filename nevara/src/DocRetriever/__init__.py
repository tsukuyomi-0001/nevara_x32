from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import ( TextLoader, UnstructuredPDFLoader, 
                                                UnstructuredWordDocumentLoader, UnstructuredPowerPointLoader,
                                                CSVLoader)
from pathlib import Path

class Document_Retriever:
    def __init__(self):
        self.embedding_model = OllamaEmbeddings(model="mxbai-embed-large")
        self.vector_store = FAISS.from_documents([Document(page_content="SAMPLE!")], self.embedding_model)
        self.resources_dir = Path("./res").absolute()

    def __document_parser(self, document: Path):
        ext = document.suffix.lower()
        if ext in [".c", ".c++", ".rs", ".py", ".html", ".css", ".js", ".tsx", ".jsx", ".c#", ".cpp", ".txt", ".toml", ".gitignore", ".python-version", ".md", ".lock"]: return TextLoader(document).load()
        elif ext == ".csv": 
            return CSVLoader(document).load()
        elif ext in [".ppt", ".pptx"]: 
            return UnstructuredPowerPointLoader(document).load()
        elif ext in [".doc", ".docx"]: 
            return UnstructuredWordDocumentLoader(document).load()
        elif ext == ".pdf": 
            return UnstructuredPDFLoader(document).load()

        return []

    def remake_vector_db(self):
        documents = []

        if not self.resources_dir.exists():
            print(f"⚠️ Warning: Directory {self.resources_dir} does not exist.")
            return

        for document in self.resources_dir.glob("*"):
            if document.is_dir(): continue
            parsed_docs = self.__document_parser(document)

            if parsed_docs: documents.extend(parsed_docs)
            else: print(f"⏩ Skipped or unsupported file type: {document.name}")

        if not documents:
            print("❌ Error: No valid documents found or parsed. Vector store was not updated.")
            return

        self.vector_store = FAISS.from_documents(documents, self.embedding_model)

    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={'k': 5})