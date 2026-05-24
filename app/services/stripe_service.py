"""
Dummy payment service — no external dependencies.
Simulates a payment intent for demo purposes.
"""
import uuid


def create_payment_intent(amount_usd: float, metadata: dict) -> dict:
    """
    Returns a fake PaymentIntent dict that mimics the structure
    used by the rest of the app (only .id is consumed).
    """
    return {
        "id": f"pi_demo_{uuid.uuid4().hex[:16]}",
        "amount": int(round(amount_usd * 100)),   # cents, for reference
        "currency": "usd",
        "status": "requires_payment_method",
        "metadata": metadata,
    }
