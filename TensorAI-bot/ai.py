import httpx
from config import *

URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}


async def ask_ai(messages):

    payload = {
        "model": MODEL,
        "messages": messages
    }

    timeout = httpx.Timeout(60)

    async with httpx.AsyncClient(timeout=timeout) as client:

        response = await client.post(
            URL,
            headers=HEADERS,
            json=payload
        )

        response.raise_for_status()

        data = response.json()

        return data["choices"][0]["message"]["content"]