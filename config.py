import os
from typing import List

API_ID = os.environ.get("API_ID", "27705761")
API_HASH = os.environ.get("API_HASH", "822cb334ca4527a134aae97f9fe44fd6")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "7688784612:AAHYx-m4tl_WeLpl7e_kskFSKUhWdFzMMzI")
ADMIN = int(os.environ.get("ADMIN", "6987158459"))

LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1002492877612"))
NEW_REQ_MODE = os.environ.get("NEW_REQ_MODE", "False").lower() == "true"  # Set "True" For accept new requests

DB_URI = os.environ.get("DB_URI", "mongodb+srv://akashrabha2005:781120@cluster0.pv6yd2f.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DB_NAME = os.environ.get("DB_NAME", "AxomBotz")

IS_FSUB = os.environ.get("IS_FSUB", "false").lower() == "true"  # Set "True" For Enable Force Subscribe
AUTH_CHANNELS = list(map(int, os.environ.get("AUTH_CHANNEL", "-1002013038353 -1002108042638").split())) # Add Multiple channel ids
