import uuid
import logging
from typing import List
from fastapi import APIRouter, Depends
from langchain_core.messages import HumanMessage

from app.agents.graph import compile_graph
from app.schemas.chat import ChatRequest, ChatResponse
from app.core.security import get_current_user_optional
from app.core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/chat", tags=["AI Chat"])

graph = compile_graph()

@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest, 
    current_user: dict | None = Depends(get_current_user_optional)
):
    thread_id = request.thread_id or str(uuid.uuid4())
    user_id = str(current_user["_id"]) if current_user else None
    
    config = {
        "configurable": {
            "thread_id": thread_id,
            "user_id": user_id
        },
        "recursion_limit": settings.AGENT_MAX_ITERATIONS
    }
    
    inputs = {"messages": [HumanMessage(content=request.message)]}
    
    try:
        logger.info(f"Invoking agentic graph for thread_id={thread_id}, user_id={user_id}")
        result = await graph.ainvoke(inputs, config=config)
        
        response_msg = result["messages"][-1].content
        if isinstance(response_msg, list):
            response_msg = "\n".join([item["text"] for item in response_msg if isinstance(item, dict) and "text" in item])
            if not response_msg:
                response_msg = str(result["messages"][-1].content)
        logger.info(f"Agent graph execution completed successfully for thread_id={thread_id}")
    except Exception as e:
        logger.error(f"[Chat Error] {type(e).__name__} for thread_id {thread_id}: {e}", exc_info=True)
        response_msg = (
            "I sincerely apologize, but I'm having a little trouble retrieving that information right now. "
            "Please rest assured that our team is looking into it. In the meantime, is there anything else I can help you plan?"
        )
    
    return ChatResponse(
        thread_id=thread_id,
        response=response_msg
    )
