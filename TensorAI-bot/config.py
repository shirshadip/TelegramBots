import json
import os
import sys

from dotenv import load_dotenv

load_dotenv()

# -------------------------------
# Load config.json
# -------------------------------
config = {}
config_path = os.path.join(os.path.dirname(__file__), "config.json")

if os.path.isfile(config_path):
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in config.json: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Failed to load config.json: {e}")
        sys.exit(1)

# -------------------------------
# Required credentials
# -------------------------------
BOT_TOKEN = (
    os.getenv("BOT_TOKEN")
    or config.get("BOT_TOKEN")
)

OPENROUTER_API_KEY = (
    os.getenv("OPENROUTER_API_KEY")
    or config.get("OPENROUTER_API_KEY")
)

# -------------------------------
# Default model fallback order
# -------------------------------
DEFAULT_MODELS = [
    "meta-llama/llama-3.3-70b-instruct:free",
    "deepseek/deepseek-r1:free",
    "qwen/qwen3-32b:free",
    "mistralai/mistral-small-3.2-24b-instruct:free",
    "openai/gpt-4o-mini",
]

# -------------------------------
# Load custom model list
# -------------------------------
raw_models = (
    os.getenv("MODELS")
    or config.get("MODELS")
)

if isinstance(raw_models, str):
    models = [m.strip() for m in raw_models.split(",") if m.strip()]
elif isinstance(raw_models, list):
    models = [str(m).strip() for m in raw_models if str(m).strip()]
else:
    models = []

# Single MODEL gets highest priority
single_model = (
    os.getenv("MODEL")
    or config.get("MODEL")
)

if single_model:
    models.insert(0, single_model.strip())

# Remove duplicates while preserving order
seen = set()
MODELS = []

for model in models + DEFAULT_MODELS:
    if model and model not in seen:
        MODELS.append(model)
        seen.add(model)

# Primary model
MODEL = MODELS[0]

# -------------------------------
# Other settings
# -------------------------------
try:
    MAX_HISTORY = int(
        os.getenv("MAX_HISTORY")
        or config.get("MAX_HISTORY", 10)
    )
except (TypeError, ValueError):
    MAX_HISTORY = 10

# -------------------------------
# Validation
# -------------------------------
if not BOT_TOKEN:
    print("Error: BOT_TOKEN is missing.")
    sys.exit(1)

if not OPENROUTER_API_KEY:
    print("Error: OPENROUTER_API_KEY is missing.")
    sys.exit(1)