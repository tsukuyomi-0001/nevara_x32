from DocRetriever import Document_Retriever
from Loader import ImageLoader

image_loader = ImageLoader()

document_retriever = Document_Retriever()
document_retriever.remake_vector_db()

message_history = []