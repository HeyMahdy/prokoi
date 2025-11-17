from typing import Annotated
from typing_extensions import TypedDict


from typing import Optional, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing_extensions import Annotated, TypedDict
from operator import add


class CareerAdvisorState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    user_id: str                
    user_profile: dict | None
    resource_progress: dict | None
    skill_tests: dict | None
    recommendations: dict | None