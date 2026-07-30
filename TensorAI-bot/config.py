import os
import json
import sys
from dotenv import load_dotenv

load_dotenv()

config = {}
config_path = os.path.join(os.path.dirname(__file__), "config.json")

if os.path.exists(config_path):
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except json.JSONDecodeError:
        print("config.json contains invalid JSON.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected configuration error: {e}")
        sys.exit(1)

BOT_TOKEN = os.getenv("BOT_TOKEN") or config.get("BOT_TOKEN")
OPENROUTER_API_KEY = (
    os.getenv("OPENROUTER_API_KEY")
    or config.get("OPENROUTER_API_KEY")
)
MODEL = os.getenv("MODEL") or config.get("MODEL", "gpt-4o-mini")

try:
    MAX_HISTORY = int(os.getenv("MAX_HISTORY") or config.get("MAX_HISTORY", 10))
except (TypeError, ValueError):
    MAX_HISTORY = 10

if not BOT_TOKEN:
    print("BOT_TOKEN is missing in both .env and config.json.")
    sys.exit(1)

if not OPENROUTER_API_KEY:
    print("OPENROUTER_API_KEY is missing in both .env and config.json.")
    sys.exit(1)
