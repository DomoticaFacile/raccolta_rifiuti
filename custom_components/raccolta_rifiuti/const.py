"""Constants for the Raccolta Rifiuti integration."""

# Creato da domoticafacile.it

DOMAIN = "raccolta_rifiuti"
PLATFORMS = ["sensor"]

# Configuration keys
CONF_CALENDAR = "calendar_entity_id"
CONF_SENSOR_NAME = "sensor_name"
CONF_LOOKAHEAD_DAYS = "lookahead_days"

# Default values
DEFAULT_SENSOR_NAME = "Raccolta Rifiuti"
DEFAULT_LOOKAHEAD_DAYS = 7

# Event type keywords and corresponding image files (case-insensitive)
EVENT_TYPE_KEYWORDS = {
    "plastica": "plastica.png",
    "umido": "umido.png",
    "organico": "umido.png",
    "indifferenziata": "indifferenziata.png",
    "indifferenziato": "indifferenziata.png",
    "secco": "indifferenziata.png",
    "rifiuto secco": "indifferenziata.png",
    "carta": "carta.png",
    "cartone": "carta.png",
    "vetro": "vetro.png",
    "metallo": "metallo.png",
    "Raccolta Sconosciuta": "vetro.png",
    # Aggiungi qui altre keyword se necessario (es. "matallo", "latta")
    # "metallo": "metallo.png",
    # "latta": "latta.png",
}

# Default image
DEFAULT_IMAGE = "default.png"

# Image path
IMAGE_BASE_PATH = "/local/images/img_raccolta_rifiuti/"

# Attributes
ATTR_EVENT_SUMMARY = "event_summary"
ATTR_EVENT_START_TIME = "event_start_time"
ATTR_DAYS_REMAINING = "days_remaining"
ATTR_COLLECTION_TYPES = "collection_types"

# Sensor States
STATE_NO_EVENT = "Nessuna raccolta programmata"
STATE_UNKNOWN_EVENT = "Raccolta sconosciuta"
