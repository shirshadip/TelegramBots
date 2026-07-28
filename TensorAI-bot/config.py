import os
import json
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")

try:

    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)

    BOT_TOKEN = os.getenv(
        "BOT_TOKEN",
        config["BOT_TOKEN"]
    )

    OPENROUTER_API_KEY = os.getenv(
        "OPENROUTER_API_KEY",
        config["OPENROUTER_API_KEY"]
    )

    MODEL = config.get(
        "MODEL",
        "google/gemma-3-27b-it"
    )

    MAX_HISTORY = config.get(
        "MAX_HISTORY",
        10
    )

except Exception as e:
    print(e)
    sys.exit()