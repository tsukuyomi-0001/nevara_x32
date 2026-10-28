from langchain_core.messages import HumanMessage, AIMessageChunk
from Agents.ConvAgent import ConverstationAgent, ConvAgentState
from nevara.globalOp import image_loader, message_history
from langchain_core.runnables import RunnableConfig
from Agents import SystemAgent

def agent_invoke(message: str):
    inState = ConvAgentState(converstation=[HumanMessage(message)])
    response = ConverstationAgent.invoke(inState)
    return response['converstation'][-1].content

def processed_text_stream(chunk):
    message, metadata = chunk

    if not isinstance(message, AIMessageChunk):
        return

    msg_json = {
        "chunk": "",
        "end": False,
        "tool": "",
        "parameter": "",
    }

    # Tool calls are part of the model response,
    # not proof that the entire graph has finished.
    if message.tool_calls:
        for tc in message.tool_calls:
            yield {
                **msg_json,
                "tool": tc.get("name", ""),
                "parameter": tc.get("args", ""),
            }

    msg_json["chunk"] = message.content or ""

    # Do NOT set end=True from chunk_position.
    if msg_json["chunk"]:
        yield msg_json

async def agent_stream(message: str):
    human_message = HumanMessage(content=message)
    config = RunnableConfig({"configurable": {"thread_id": "your-unique-session-id"}})
    print(message_history)

    inState = ConvAgentState(
        converstation=[*message_history, image_loader.apply_images(human_message)]
    )

    async for mode, data in ConverstationAgent.astream(
        inState,
        config=config,
        stream_mode=["messages", "updates"],
    ):
        if mode == "messages":
            for event in processed_text_stream(data):
                yield event

    yield {
        "chunk": "",
        "end": True,
        "tool": "",
        "parameter": "",
    }

    message_history.extend([human_message, ConverstationAgent.get_state(config).values['converstation'][-1]])

def main() -> None:
    system_agent_interface = SystemAgent.Interface()
    # system_agent_interface.initalize()