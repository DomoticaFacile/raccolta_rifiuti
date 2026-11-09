# Creato da domoticafacile.it

DOMAIN = "raccolta_rifiuti"
PLATFORMS = ["sensor"]

# Config entry data/options keys (CONF_NAME comes from homeassistant.const).

CONF_CALENDAR = "calendar_entity_id"
CONF_LOOKAHEAD_DAYS = "lookahead_days"
CONF_LANGUAGE = "language"

DEFAULT_LOOKAHEAD_DAYS = 7
MAX_LOOKAHEAD_DAYS = 60
DEFAULT_TITLE = "Raccolta Rifiuti"

# "auto" = use Home Assistant's configured language (hass.config.language),
# falling back to English if it isn't one of the supported languages.
CONF_LANGUAGE_AUTO = "auto"
DEFAULT_LANGUAGE_OPTION = CONF_LANGUAGE_AUTO

# Image path (served from config/www/... via the /local/ alias)
IMAGE_BASE_PATH = "/local/images/img_raccolta_rifiuti/"

# Attributes describing TODAY's calendar entry (unchanged contract).
ATTR_EVENT_SUMMARY = "event_summary"
ATTR_EVENT_START_TIME = "event_start_time"
ATTR_COLLECTION_TYPES = "collection_types"
# Language-independent version of collection_types (canonical English
# identifiers, e.g. "paper", "glass"), stable regardless of `language:`.
ATTR_COLLECTION_TYPE_CODES = "collection_type_codes"

# Attributes describing the NEXT upcoming collection within lookahead_days
# (0 days away if today has one, otherwise the first matching day ahead).
ATTR_DAYS_REMAINING = "days_remaining"
ATTR_NEXT_COLLECTION_DATE = "next_collection_date"
ATTR_NEXT_COLLECTION_TYPES = "next_collection_types"
ATTR_NEXT_COLLECTION_TYPE_CODES = "next_collection_type_codes"


# --- Telegram notifications (options of the config entry) -------------------
CONF_TELEGRAM_ENABLED = "telegram_enabled"
# notify entities created by Home Assistant's Telegram bot integration
# (one per allowed chat), e.g. ["notify.my_bot_family_chat"].
CONF_TELEGRAM_TARGETS = "telegram_targets"
CONF_NOTIFY_TIME = "notify_time"
CONF_NOTIFY_SECOND_ENABLED = "notify_second_enabled"
CONF_NOTIFY_SECOND_TIME = "notify_second_time"
CONF_NOTIFY_LANGUAGE = "notify_language"
CONF_NOTIFY_EMOJI = "notify_emoji"
CONF_NOTIFY_TITLE = "notify_title"

DEFAULT_NOTIFY_TIME = "20:00:00"
DEFAULT_NOTIFY_SECOND_TIME = "20:30:00"

TELEGRAM_DOMAIN = "telegram_bot"


def sensor_unique_id(calendar_entity_id: str) -> str:
    """Unique id of the collection sensor.

    Kept identical to the one used by the YAML-based versions, so that an
    existing sensor keeps its entity_id and history when it is migrated to a
    config entry.
    """
    return f"{DOMAIN}_{calendar_entity_id}_next_collection"
