from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.state import StateGraph, END
from langchain_core.messages import SystemMessage
from Agents.ConvAgent.tools import sacred_tools
from langgraph.prebuilt import ToolNode
from .schema import ConvAgentState
from datetime import datetime
from .model import model
import os

tool_node = ToolNode(sacred_tools, messages_key="converstation")

def Brain(state: ConvAgentState):
    system_message = SystemMessage(f"""
    [Personal Info]
    Your are Helpful assistant, and your name is Nevara.

    follow following steps:
    1) reason whether you know the answer or not. if yes answer user directly if not proceed to 2nd step.
    2) if you don't have the answer, you your tools to get, for example if user is asking for document use retriever tool if and only if document is mentioned in your world state, or use DuckDuckGo Result to get answers from internet.
    3) if you believe answer can't be determined or is unable to find, simply tell user that you don't know or you couldn't find proper solution to it.

    [World Knowledge]
    Today's Date: {datetime.now().strftime("%d/%m/%Y  (dd,mm,yyyy)")}
    Current Time: {datetime.now().strftime("%I:%M %p  (HH:MM AM/PM)")}
    
    *User uploaded following files into Retriever Bank: {os.listdir("./res")}
    """)
    
    response = model.invoke([system_message, *state.converstation])
    # if response.tool_calls: return Command(goto='ToolNode', update={ 'converstation': [*state.converstation, response] })
    return { 'converstation': [*state.converstation, response] }

def route_after_brain(state: ConvAgentState):
    last_message = state.converstation[-1]

    if last_message.tool_calls:
        return "ToolNode"

    return END

graph = StateGraph(ConvAgentState)
graph.add_node("Brain", Brain)
graph.add_node("ToolNode", tool_node)
graph.set_entry_point("Brain")
graph.add_conditional_edges(
    "Brain",
    route_after_brain,
    {
        "ToolNode": "ToolNode",
        END: END,
    },
)
graph.add_edge('ToolNode', 'Brain')

checkpointer = InMemorySaver()
ConverstationAgent = graph.compile(checkpointer=checkpointer)