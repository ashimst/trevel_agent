import uuid
from typing import List
from fastapi import APIRouter, Depends
from langchain_core.messages import HumanMessage

from app.agents.graph import compile_graph
from app.schemas.chat import ChatRequest, ChatResponse
from app.core.security import get_current_user_optional

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
        }
    }
    
    inputs = {"messages": [HumanMessage(content=request.message)]}
    
    try:
        # Checkpointer is already baked into the compiled graph
        result = await graph.ainvoke(inputs, config=config)
        
        response_msg = result["messages"][-1].content
        if isinstance(response_msg, list):
            response_msg = "\n".join([item["text"] for item in response_msg if isinstance(item, dict) and "text" in item])
            if not response_msg:
                response_msg = str(result["messages"][-1].content)
    except Exception as e:
        print(f"[Chat Error] {type(e).__name__}: {e}")
        response_msg = "I'm sorry, I encountered an issue processing your request. Could you please try rephrasing your question?"
    
    return ChatResponse(
        thread_id=thread_id,
        response=response_msg
    )
