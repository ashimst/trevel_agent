from langgraph.graph import StateGraph, START, END
from langchain_core.runnables.config import RunnableConfig

from app.agents.state import AgentState
from app.agents.supervisor import create_supervisor
from app.agents.memory import get_checkpointer
from app.agents.sub_agents import (
    create_planner_agent,
    create_booking_agent,
    create_support_agent,
    create_recommender_agent,
    create_trip_organizer_agent
)

def _wrap_agent(agent):
    """Wraps a compiled react agent to only return the new messages."""
    async def _node(state: AgentState, config: RunnableConfig):
        result = await agent.ainvoke({"messages": state["messages"]}, config)
        original_length = len(state["messages"])
        new_messages = result["messages"][original_length:]
        return {"messages": new_messages}
    return _node

def compile_graph():
    builder = StateGraph(AgentState)
    
    # 1. Add Nodes
    builder.add_node("supervisor", create_supervisor())
    
    planner_agent = create_planner_agent()
    builder.add_node("travel_planner", _wrap_agent(planner_agent))
    
    booking_agent = create_booking_agent()
    builder.add_node("booking_agent", _wrap_agent(booking_agent))
    
    support_agent = create_support_agent()
    builder.add_node("support_agent", _wrap_agent(support_agent))
    
    recommender_agent = create_recommender_agent()
    builder.add_node("recommendation_agent", _wrap_agent(recommender_agent))
    
    trip_organizer_agent = create_trip_organizer_agent()
    builder.add_node("trip_organizer", _wrap_agent(trip_organizer_agent))
    
    # 2. Add Edges
    # The graph always starts at the supervisor
    builder.add_edge(START, "supervisor")
    
    # The supervisor decides which agent to call next
    def route_supervisor(state: AgentState):
        next_agent = state.get("next_agent", "FINISH")
        if next_agent == "FINISH":
            return END
        return next_agent
        
    builder.add_conditional_edges(
        "supervisor",
        route_supervisor,
        {
            "travel_planner": "travel_planner",
            "booking_agent": "booking_agent",
            "support_agent": "support_agent",
            "recommendation_agent": "recommendation_agent",
            "trip_organizer": "trip_organizer",
            END: END
        }
    )
    
    # After a sub-agent handles the user request, it's done. 
    # The next human message will trigger a new run starting from START.
    builder.add_edge("travel_planner", END)
    builder.add_edge("booking_agent", END)
    builder.add_edge("support_agent", END)
    builder.add_edge("recommendation_agent", END)
    builder.add_edge("trip_organizer", END)
    
    # Compile with checkpointer for persistent memory
    checkpointer = get_checkpointer()
    return builder.compile(checkpointer=checkpointer)

