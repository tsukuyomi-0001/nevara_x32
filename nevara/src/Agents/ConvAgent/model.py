from langchain_ollama import ChatOllama
from Agents.ConvAgent.tools import sacred_tools

model = ChatOllama(
    # model='qwen3.5:0.8b',
    # model="qwen3.5:4b",
    model="qwen3.5:2b",
    num_ctx=12*1024,
    keep_alive="30m"
)

model = model.bind_tools(sacred_tools)
