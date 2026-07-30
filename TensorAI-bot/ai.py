import httpx
from config import *

URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

async def ask_ai(messages):
    timeout = httpx.Timeout(60)

    async with httpx.AsyncClient(timeout=timeout) as client:

        last_error = None

        for model in MODELS:
            payload = {
                "model": model,
                "messages": messages,
            }

            try:
                print(f"Trying model: {model}")

                response = await client.post(
                    URL,
                    headers=HEADERS,
                    json=payload,
                )

                response.raise_for_status()

                data = response.json()

                return data["choices"][0]["message"]["content"]

            except httpx.HTTPStatusError as e:
                print(f"{model} failed")
                print(e.response.status_code)
                print(e.response.text)
                last_error = e

        raise last_error
    
print ("Model", model)