# -*- coding: utf-8 -*-
"""Localization data and helpers for Raccolta Rifiuti.

This module keeps waste-type recognition (what the user typed into the
calendar) separate from waste-type display (what the sensor shows).

- KEYWORDS_BY_LANGUAGE maps *source* languages -> phrase -> canonical type.
  All languages are merged together when matching, so a calendar written in
  Italian, English, or a mix of both is always recognized correctly.
- LABELS maps a *display* language -> canonical type -> localized label.
  This only affects what the sensor shows to the user (state / attributes),
  not what it recognizes.

To add a new language, add an entry to KEYWORDS_BY_LANGUAGE (recognition),
LABELS (display) and STRINGS (fixed UI text), then add the language code to
SUPPORTED_LANGUAGES.
"""

# --- Canonical (language-independent) waste type identifiers ---------------
TYPE_PAPER = "paper"
TYPE_PLASTIC = "plastic"
TYPE_GLASS = "glass"
TYPE_ORGANIC = "organic"
TYPE_RESIDUAL = "residual"
TYPE_METAL = "metal"
TYPE_GREEN = "green"
TYPE_UNKNOWN = "unknown"

# Image file associated with each canonical type (files already shipped
# under images/img_raccolta_rifiuti/).
TYPE_IMAGES = {
    TYPE_PAPER: "carta.png",
    TYPE_PLASTIC: "plastica.png",
    TYPE_GLASS: "vetro.png",
    TYPE_ORGANIC: "umido.png",
    TYPE_RESIDUAL: "indifferenziata.png",
    TYPE_METAL: "metallo.png",
    TYPE_GREEN: "verde.png",
}

DEFAULT_IMAGE = "default.png"

# --- Recognition: phrases the user might write in the calendar -------------
# Longer/more specific phrases are tried before shorter ones (handled by the
# caller sorting by length), so e.g. "rifiuto secco" wins over "secco".
KEYWORDS_BY_LANGUAGE = {
    "it": {
        "carta": TYPE_PAPER,
        "cartone": TYPE_PAPER,
        "plastica": TYPE_PLASTIC,
        "vetro": TYPE_GLASS,
        "umido": TYPE_ORGANIC,
        "organico": TYPE_ORGANIC,
        "frazione organica": TYPE_ORGANIC,
        "indifferenziata": TYPE_RESIDUAL,
        "indifferenziato": TYPE_RESIDUAL,
        "secco": TYPE_RESIDUAL,
        "rifiuto secco": TYPE_RESIDUAL,
        "metallo": TYPE_METAL,
        "lattine": TYPE_METAL,
        "verde": TYPE_GREEN,
        "sfalci": TYPE_GREEN,
        "potature": TYPE_GREEN,
        "vegetale": TYPE_GREEN,
    },
    "en": {
        "paper": TYPE_PAPER,
        "cardboard": TYPE_PAPER,
        "plastic": TYPE_PLASTIC,
        "glass": TYPE_GLASS,
        "organic": TYPE_ORGANIC,
        "food waste": TYPE_ORGANIC,
        "wet waste": TYPE_ORGANIC,
        "residual": TYPE_RESIDUAL,
        "mixed waste": TYPE_RESIDUAL,
        "general waste": TYPE_RESIDUAL,
        "metal": TYPE_METAL,
        "cans": TYPE_METAL,
        "green waste": TYPE_GREEN,
        "garden waste": TYPE_GREEN,
        "yard waste": TYPE_GREEN,
    },
}

# --- Display: what the sensor shows, per output language --------------------
LABELS = {
    "it": {
        TYPE_PAPER: "Carta",
        TYPE_PLASTIC: "Plastica",
        TYPE_GLASS: "Vetro",
        TYPE_ORGANIC: "Umido",
        TYPE_RESIDUAL: "Indifferenziata",
        TYPE_METAL: "Metallo",
        TYPE_GREEN: "Verde",
        TYPE_UNKNOWN: "Raccolta sconosciuta",
    },
    "en": {
        TYPE_PAPER: "Paper",
        TYPE_PLASTIC: "Plastic",
        TYPE_GLASS: "Glass",
        TYPE_ORGANIC: "Organic",
        TYPE_RESIDUAL: "Residual waste",
        TYPE_METAL: "Metal",
        TYPE_GREEN: "Green waste",
        TYPE_UNKNOWN: "Unknown collection",
    },
}

# Fixed sensor text (name, states) per output language.
STRINGS = {
    "it": {
        "default_name": "Raccolta Rifiuti",
        "no_event": "Nessuna raccolta programmata",
        "calendar_not_found": "Calendario non trovato",
        "service_error": "Errore servizio calendario",
    },
    "en": {
        "default_name": "Waste Collection",
        "no_event": "No collection scheduled",
        "calendar_not_found": "Calendar not found",
        "service_error": "Calendar service error",
    },
}

DEFAULT_LANGUAGE = "en"
SUPPORTED_LANGUAGES = ("it", "en")


def resolve_language(preferred):
    """Return a supported language code, falling back to English.

    `preferred` can be None, an explicit code ("it", "en"), or a locale
    like "it-IT" (as returned by hass.config.language) — only the primary
    subtag is considered.
    """
    if preferred:
        lang = preferred.split("-")[0].lower()
        if lang in SUPPORTED_LANGUAGES:
            return lang
    return DEFAULT_LANGUAGE


def build_keyword_index():
    """Merge keywords from every source language into one lookup dict.

    This is intentionally language-agnostic on the *recognition* side: a
    calendar can mix Italian and English event names and both are matched,
    independently of which language is chosen for display.
    """
    merged = {}
    for lang_keywords in KEYWORDS_BY_LANGUAGE.values():
        merged.update(lang_keywords)
    return merged
