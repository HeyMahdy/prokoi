
import json
from langchain_core.messages import ToolMessage
from src.ai.tool import tools_by_name
from src.ai.state import CareerAdvisorState


def tool_node_01(state: CareerAdvisorState):
    """Execute all tool calls from the last message in the state."""
    outputs = []
    for tool_call in state["messages"][-1].tool_calls:
        # Handle both sync and async tools
        tool = tools_by_name[tool_call["name"]]
        if hasattr(tool, 'coroutine') and tool.coroutine:
            # For async tools, we need to await the result
            import asyncio
            tool_result = asyncio.run(tool.ainvoke(tool_call["args"]))
        else:
            # For sync tools, use invoke
            tool_result = tool.invoke(tool_call["args"])
        outputs.append(
            ToolMessage(
                content=json.dumps(tool_result),
                name=tool_call["name"],
                tool_call_id=tool_call["id"],
            )
        )
    return {"messages": outputs}