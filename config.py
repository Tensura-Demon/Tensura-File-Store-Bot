# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

import os

def must_get(name):
    value = os.getenv(name)
    if not value:
        raise Exception(f"{name} is not set in environment variables")
    return value.strip()

# ------------------------- #
# CORE CONFIG
# ------------------------- #

API_ID = int(must_get("API_ID"))
API_HASH = must_get("API_HASH")
BOT_TOKEN = must_get("BOT_TOKEN")

# ------------------------- #
# DATABASE
# ------------------------- #

MONGO_URI = must_get("MONGO_URI")

# ------------------------- #
# BOT INFO
# ------------------------- #

BOT_USERNAME = must_get("BOT_USERNAME")

CHANNEL_ID = int(must_get("CHANNEL_ID"))
LOG_CHANNEL = int(must_get("LOG_CHANNEL"))

# ------------------------- #
# OWNER
# ------------------------- #

OWNER_ID = int(must_get("OWNER_ID"))

# ------------------------- #
# SERVER
# ------------------------- #

PORT = int(os.getenv("PORT", "10000"))
