from typing import Literal
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from app.agents.llms import get_supervisor_llm
from app.agents.state import AgentState

class RouteDecision(BaseModel):
    next: Literal["travel_planner", "booking_agent", "support_agent", "recommendation_agent", "trip_organizer", "FINISH"]
    reasoning: str

def create_supervisor():
    llm = get_supervisor_llm()
    
    system_prompt = (
        "You are the supervisor of a multi-agent travel agency system. "
        "Your ONLY job is to route the user's request to the correct specialized agent.\n\n"
        "Available agents:\n"
        "- travel_planner: For searching flights, buses, hotels, and activities.\n"
        "- booking_agent: For booking, confirming, or cancelling reservations, and checking user bookings.\n"
        "- support_agent: For answering general questions, greetings, or checking payment status.\n"
        "- recommendation_agent: For creative travel advice, searching guides or car rentals, and live travel trends.\n"
        "- trip_organizer: For creating trips, managing trip itineraries, and grouping bookings.\n\n"
        "RULES:\n"
        "1. You MUST output one of the exact names above or FINISH.\n"
        "2. Output FINISH if the conversation is just beginning with a greeting, or if the request has been fully answered.\n"
        "3. For greetings like 'hi', 'hello' → route to support_agent.\n"
        "4. NEVER output 'supervisor' or any name not in the list above.\n"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("placeholder", "{messages}"),
    ])
    
    # We use structured output to force the LLM to return RouteDecision
    supervisor_chain = prompt | llm.with_structured_output(RouteDecision)
    
    async def supervisor_node(state: AgentState):
        try:
            decision = await supervisor_chain.ainvoke(state)
            return {"next_agent": decision.next}
        except Exception as e:
            # Fallback: route to support_agent on any parsing/validation failure
            print(f"[Supervisor Fallback] Error: {e}")
            return {"next_agent": "support_agent"}
        
    return supervisor_node
