"""
Shared helpers for all service routers.
Converts MongoDB ObjectId docs to response-friendly dicts.
"""
from bson import ObjectId


def serialize_doc(doc: dict) -> dict:
    """Remap _id → id and stringify ObjectIds."""
    out = {k: v for k, v in doc.items()}
    if "_id" in out:
        out["id"] = str(out.pop("_id"))
    # Stringify any remaining ObjectId values
    for k, v in out.items():
        if isinstance(v, ObjectId):
            out[k] = str(v)
    return out


async def list_collection(db, collection: str, skip: int = 0, limit: int = 20) -> list[dict]:
    cursor = db[collection].find().skip(skip).limit(limit)
    return [serialize_doc(d) async for d in cursor]


async def get_one(db, collection: str, doc_id: str) -> dict | None:
    doc = await db[collection].find_one({"_id": ObjectId(doc_id)})
    return serialize_doc(doc) if doc else None
