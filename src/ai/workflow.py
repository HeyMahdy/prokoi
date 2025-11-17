from src.ai.tool_node import tool_node_01
from langgraph.graph import StateGraph, START, END
from src.ai.agent import CareerAdvisorAgent 
from src.ai.state import CareerAdvisorState

# Initialize the graph
workflow = StateGraph(CareerAdvisorState)

# Add nodes
workflow.add_node("career_advisor", CareerAdvisorAgent)
workflow.add_node("tools", tool_node_01)

# Routing function
def route_after_agent(state: CareerAdvisorState):
    """
    Route based on whether agent wants to call tools or is done.
    """
    messages = state["messages"]
    last_message = messages[-1]
    
    # If agent wants to call tools
    if getattr(last_message, "tool_calls", None):
        return "tools"
    
    # If agent is done (has final recommendations)
    return END

# Define the flow
workflow.add_edge(START, "career_advisor")  # Start with agent

workflow.add_conditional_edges(
    "career_advisor",
    route_after_agent,
    {
        "tools": "tools",  # Agent wants to call tools
        END: END,          # Agent is done
    },
)

workflow.add_edge("tools", "career_advisor")  # After tools, go back to agent

# Compile the graph
graph = workflow.compile()