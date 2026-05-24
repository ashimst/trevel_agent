import warnings
from pymongo import MongoClient
from langgraph.checkpoint.mongodb import MongoDBSaver
from app.core.config import settings

# Suppress the pending deprecation warning from LangGraph serializer
warnings.filterwarnings("ignore", module="langgraph.cache.base")
warnings.filterwarnings("ignore", message=".*allowed_objects.*")

_sync_client = None

def get_checkpointer() -> MongoDBSaver:
    global _sync_client
    if _sync_client is None:
        _sync_client = MongoClient(settings.MONGODB_URL)
        
    return MongoDBSaver(
        client=_sync_client, 
        db_name=settings.CHECKPOINT_DB_NAME
    )
