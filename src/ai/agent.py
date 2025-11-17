from src.ai.prompts import system_message_career_advisor
from typing import Any
from src.ai.state import CareerAdvisorState
from src.ai.llm_store import get_llm as _get_llm

# Initialize the model with tools
_model_with_tools = None

def CareerAdvisorAgent(state: CareerAdvisorState):
    global _model_with_tools
    if _model_with_tools is None:
        _model_with_tools = _get_llm().bind_tools(tools)

    model = system_message_career_advisor | _model_with_tools
    response = model.invoke({
        "agent_scratchpad": state["messages"],
        "user_id": state["user_id"],
    })
    return {"messages": [response]}
