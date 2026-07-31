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
        print(f"❌ Invalid JSON in config.json: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Failed to load config.json: {e}")
        sys.exit(1)

# -------------------------------
# Required credentials
# -------------------------------
BOT_TOKEN = (
    os.getenv("BOT_TOKEN")
    or config.get("BOT_TOKEN")
)

NVIDIA_API_KEY = (
    os.getenv("NVIDIA_API_KEY")
    or config.get("NVIDIA_API_KEY")
)

# -------------------------------
# Default model fallback order
# Use official NVIDIA model identifiers
# -------------------------------
DEFAULT_MODELS = [
    "nvidia/nemotron-3-super-128b-instruct-qwen",
    "nvidia/nemotron-4-340b-instruct",
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

# Primary model (for reference)
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

# Ensure MAX_HISTORY is at least 2 (1 for system, 1 for actual chat)
if MAX_HISTORY < 2:
    MAX_HISTORY = 2

# -------------------------------
# Validation
# -------------------------------
if not BOT_TOKEN:
    print("❌ Error: BOT_TOKEN is missing.")
    print("   Set it in .env or config.json")
    sys.exit(1)

if not NVIDIA_API_KEY:
    print("❌ Error: NVIDIA_API_KEY is missing.")
    print("   Set it in .env or config.json")
    print("   Get your API key from: https://build.nvidia.com/")
    sys.exit(1)

if not MODELS:
    print("❌ Error: No models configured.")
    print("   Add MODEL or MODELS to .env or config.json")
    sys.exit(1)

# Print startup info
print("✅ Configuration loaded successfully")
print(f"   BOT_TOKEN: {'***' + BOT_TOKEN[-4:] if len(BOT_TOKEN) > 4 else '***'}")
print(f"   NVIDIA_API_KEY: {'***' + NVIDIA_API_KEY[-8:] if len(NVIDIA_API_KEY) > 8 else '***'}")
print(f"   Available models: {len(MODELS)}")
print(f"   Primary model: {MODEL}")
print(f"   Max history: {MAX_HISTORY}")