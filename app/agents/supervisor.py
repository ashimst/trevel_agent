import logging
from typing import Literal
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from app.agents.llms import get_supervisor_llm
from app.agents.state import AgentState

logger = logging.getLogger(__name__)

class RouteDecision(BaseModel):
    next: Literal["travel_planner", "booking_agent", "support_agent", "recommendation_agent", "trip_organizer", "FINISH"] = Field(
        description="The next agent to route to, or FINISH if the user request has been fully handled and resolved."
    )
    reasoning: str = Field(
        description="Detailed logical reasoning explaining why this routing choice is selected based on the conversation history."
    )

def create_supervisor():
    llm = get_supervisor_llm()
    
    system_prompt = (
        "You are the supervisor of a multi-agent travel agency system. "
        "Your ONLY job is to route the conversation to the correct specialized agent based on the user's message "
        "and the preceding conversation context.\n\n"
        "Available agents and their specific areas of expertise:\n"
        "- travel_planner: For searching inventory for flights, buses, hotels, activities, and guides. "
        "Use this agent when the user is asking to search, look up, or find details about flights, hotels, or buses "
        "to a destination.\n"
        "- booking_agent: For creating new bookings (flights, buses, hotels, etc.), confirming pending reservations, "
        "or cancelling existing bookings. Use this when the user says 'book that', 'confirm reservation', 'cancel my hotel', etc.\n"
        "- support_agent: For handling greetings (hello, hi, how are you), general help queries, payment status checks, "
        "cancellation policy questions, and general customer service. This agent provides a warm, welcoming presence.\n"
        "- recommendation_agent: For inspirational travel advice, destination ideas, suggesting things to do, "
        "checking travel guides/car rentals, and reading live web trends/weather. Use this when they want open-ended suggestions "
        "like 'where should I go for a beach holiday?' or 'tell me about things to do in Paris'.\n"
        "- trip_organizer: For managing the user's overall trips, grouping bookings together into trips, "
        "creating new trip objects, checking current trips, and compiling trip agendas.\n\n"
        "ROUTING RULES:\n"
        "1. Read the ENTIRE conversation history to understand the context. For instance, if the user says 'book it', "
        "look at the previous messages to see what they are trying to book, and route to booking_agent.\n"
        "2. Do NOT route to FINISH immediately if the user just greeted you. Route to support_agent so they get a warm welcome.\n"
        "3. Route to FINISH ONLY when the request is fully resolved, the user is saying goodbye, expressing final thanks, "
        "or when no further action is required from the system.\n"
        "4. Be accurate and explain your reasoning clearly."
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("placeholder", "{messages}"),
    ])
    
    supervisor_chain = prompt | llm.with_structured_output(RouteDecision)
    
    async def supervisor_node(state: AgentState):
        try:
            decision = await supervisor_chain.ainvoke(state)
            logger.info(f"Supervisor routed next: {decision.next}. Reasoning: {decision.reasoning}")
            return {"next_agent": decision.next}
        except Exception as e:
            logger.error(f"[Supervisor Fallback] Error: {e}", exc_info=True)
            return {"next_agent": "support_agent"}
        
    return supervisor_node
