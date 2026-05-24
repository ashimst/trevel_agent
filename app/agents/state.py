from typing import Annotated, Sequence, TypedDict, Literal
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    """The overall state for the LangGraph multi-agent system."""
    messages: Annotated[Sequence[BaseMessage], add_messages]
    next_agent: str | None
