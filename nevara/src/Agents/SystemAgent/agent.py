from langgraph.graph.state import StateGraph, Command
from .schema import SysAgentState, DecisionStucture
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import ToolNode
from .model import model
from .tool import tools
import subprocess

agent_model = model.bind_tools(tools)
router_model = model.with_structured_output(DecisionStucture)
tool_node = ToolNode(tools, messages_key="converstation")

def GetSystemLogs(state: SysAgentState):
    process = subprocess.Popen(["journalctl", "-n", "50"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()
    return { "system_logs": stdout}

def Router(state: SysAgentState):
    systemPrompt = SystemMessage(content=f"""
    Following are the Cachy linux (Arch linux) journalctl system logs
    Your Job is to decide whether system truely require system repairs or not.
    Things you need to watch for are like: kernel failure, network failure, disk/parition related, drivers, or critical system states.

    [System Logs]
    {state.system_logs}
    """)
    response = router_model.invoke([systemPrompt])
    if response.judgment: return Command(goto="Agent", update={'problem_statement': response.problem_statement})
    else: return

def Agent(state: SysAgentState):
    systemPrompt = SystemMessage(content=f"""
    You are system repairment agent.
    Your job is to search online, decide whether you should run command or not.

    Follow these steps:
    1) search online for modern methods to perform system repair for cachy os (arch linux).
    2) decide whether you have sufficient information or not to fix, if yes move to 3rd step if not move to 1st step (web searching...)
    3) after having sufficent information decide whether following command is safe to respect following: user's privacy, system damage from command.
    4) if your choice was no, than find alternative way to fix system, if your choice was yes, than run the command.
    5) onces the system is fixed, you make small report for user.

    [System Logs]
    {state.system_logs}

    [Problem Statement]
    {state.problem_statement}
    """)

    response = model.invoke([systemPrompt, *state.converstation])

    if response.tool_calls: return Command(goto="ToolNode", update={"converstation": [*state.converstation, response]})
    return {"converstation": [*state.converstation, response]}

graph = StateGraph(SysAgentState)
graph.add_node("Agent", Agent)
graph.add_node("ToolNode", tool_node)
graph.add_node("GetSystemLogs", GetSystemLogs)
graph.add_node("Router", Router)
graph.set_entry_point("GetSystemLogs")
graph.add_edge("GetSystemLogs", "Router")
graph.add_edge("ToolNode", "Agent")
SystemAgent = graph.compile()