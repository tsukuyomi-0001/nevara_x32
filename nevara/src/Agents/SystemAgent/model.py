from langchain_ollama import ChatOllama

model = ChatOllama(
    model='qwen3.5:0.8b',
    keep_alive="30m"
)

