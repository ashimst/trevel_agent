import os
if "SSL_CERT_FILE" in os.environ and not os.path.exists(os.environ["SSL_CERT_FILE"]):
    del os.environ["SSL_CERT_FILE"]

import asyncio
import httpx

async def test_chat():
    async with httpx.AsyncClient() as client:
        # 1. Search for a flight
        print("Sending message to Travel Planner...")
        response = await client.post("http://127.0.0.1:8001/chat/", json={
            "message": "Find me flights from London to Dubai"
        })
        data = response.json()
        print("Response:", data["response"])
        
        thread_id = data["thread_id"]
        
        # 2. Test booking (should ask for confirmation)
        print("\nSending booking request...")
        response = await client.post("http://127.0.0.1:8001/chat/", json={
            "message": "I want to book the Emirates flight.",
            "thread_id": thread_id
        })
        data = response.json()
        print("Response:", data["response"])

        print("\nTests completed.")

if __name__ == "__main__":
    asyncio.run(test_chat())
