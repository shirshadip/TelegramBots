import httpx
from config import NVIDIA_API_KEY, MODELS

URL = "https://integrate.api.nvidia.com/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {NVIDIA_API_KEY}",
    "Content-Type": "application/json"
}

async def ask_ai(messages):
    """
    Send messages to NVIDIA Nemotron model and get response.
    Tries models in fallback order if one fails.
    """
    timeout = httpx.Timeout(60)

    async with httpx.AsyncClient(timeout=timeout) as client:
        last_error = None

        for model in MODELS:
            payload = {
                "model": model,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 2048,
                "top_p": 0.9,
            }

            try:
                print(f"🔄 Trying model: {model}")

                response = await client.post(
                    URL,
                    headers=HEADERS,
                    json=payload,
                )

                response.raise_for_status()

                data = response.json()

                content = data["choices"][0]["message"]["content"]
                print(f"✅ Success with model: {model}")
                return content

            except httpx.HTTPStatusError as e:
                print(f"❌ {model} failed with status {e.response.status_code}")
                print(f"Error details: {e.response.text}")
                last_error = e
            
            except KeyError as e:
                print(f"❌ Unexpected response format from {model}: {e}")
                print(f"Response: {data if 'data' in locals() else 'N/A'}")
                last_error = e

        # If all models fail, raise the last error
        if last_error:
            raise last_error
        else:
            raise Exception("No models available to try")