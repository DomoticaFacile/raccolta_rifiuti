# -*- coding: utf-8 -*-
"""Evening Telegram notification for Raccolta Rifiuti."""

# Creato da domoticafacile.it
from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import CALLBACK_TYPE, HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.event import async_track_time_change
from homeassistant.util import dt as dt_util

from .config_flow import TELEGRAM_DEFAULTS, entry_config
from .const import (
    ATTR_COLLECTION_TYPE_CODES,
    CONF_CALENDAR,
    CONF_LANGUAGE_AUTO,
    CONF_NOTIFY_EMOJI,
    CONF_NOTIFY_LANGUAGE,
    CONF_NOTIFY_SECOND_ENABLED,
    CONF_NOTIFY_SECOND_TIME,
    CONF_NOTIFY_TIME,
    CONF_NOTIFY_TITLE,
    CONF_TELEGRAM_ENABLED,
    CONF_TELEGRAM_TARGETS,
    DOMAIN,
    sensor_unique_id,
)
from .localization import build_notification, resolve_language

_LOGGER = logging.getLogger(__name__)


class RaccoltaRifiutiNotifier:
    """Sends the "what to put out tomorrow" message at the configured times.

    The sensor describes the collection of the day (the calendar events are
    entered the evening before, see the README), so at the configured
    evening time its `collection_type_codes` are exactly what is picked up
    tomorrow. Nothing is sent when there is no collection.
    """

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.hass = hass
        self.entry = entry
        self._unsubscribe: list[CALLBACK_TYPE] = []

    def _config(self) -> dict[str, Any]:
        return {**TELEGRAM_DEFAULTS, **entry_config(self.entry)}

    @callback
    def async_start(self) -> None:
        """Schedule the notification times, if Telegram is enabled."""
        config = self._config()
        if not config[CONF_TELEGRAM_ENABLED]:
            _LOGGER.debug("Telegram notifications are disabled for %s", self.entry.title)
            return

        raw_times = [config[CONF_NOTIFY_TIME]]
        if config[CONF_NOTIFY_SECOND_ENABLED]:
            raw_times.append(config[CONF_NOTIFY_SECOND_TIME])

        for raw in dict.fromkeys(raw_times):  # same time twice => schedule once
            parsed = dt_util.parse_time(str(raw))
            if parsed is None:
                _LOGGER.error("Invalid notification time %r, ignoring it", raw)
                continue
            self._unsubscribe.append(
                async_track_time_change(
                    self.hass,
                    self._async_time_fired,
                    hour=parsed.hour,
                    minute=parsed.minute,
                    second=parsed.second,
                )
            )
            _LOGGER.debug("Telegram notification scheduled at %s", parsed)

    @callback
    def async_stop(self) -> None:
        """Cancel the scheduled notifications."""
        while self._unsubscribe:
            self._unsubscribe.pop()()

    async def _async_time_fired(self, _now: datetime) -> None:
        await self.async_send()

    async def async_send(self) -> bool:
        """Send the notification now. Returns True if a message was sent."""
        config = self._config()
        targets = list(config.get(CONF_TELEGRAM_TARGETS) or [])
        if not targets:
            _LOGGER.warning("Telegram notifications are enabled but no recipient is selected")
            return False

        sensor_entity_id = er.async_get(self.hass).async_get_entity_id(
            "sensor", DOMAIN, sensor_unique_id(self.entry.data[CONF_CALENDAR])
        )
        if sensor_entity_id is None:
            _LOGGER.warning("Collection sensor not found, notification skipped")
            return False

        # The sensor only polls every 30 minutes: refresh it so the message
        # reflects the calendar as it is right now.
        try:
            await self.hass.services.async_call(
                "homeassistant", "update_entity", {"entity_id": sensor_entity_id}, blocking=True
            )
        except HomeAssistantError as err:
            _LOGGER.warning("Could not refresh %s before notifying: %s", sensor_entity_id, err)

        state = self.hass.states.get(sensor_entity_id)
        codes = list(state.attributes.get(ATTR_COLLECTION_TYPE_CODES) or []) if state else []
        if not codes:
            _LOGGER.debug("No collection scheduled, no notification sent")
            return False

        language = config[CONF_NOTIFY_LANGUAGE]
        if language == CONF_LANGUAGE_AUTO:
            language = resolve_language(getattr(self.hass.config, "language", None))

        title, message = build_notification(
            codes,
            language,
            use_emoji=config[CONF_NOTIFY_EMOJI],
            custom_title=config.get(CONF_NOTIFY_TITLE),
        )

        try:
            await self.hass.services.async_call(
                "notify",
                "send_message",
                {"entity_id": targets, "message": message, "title": title},
                blocking=True,
            )
        except HomeAssistantError as err:
            _LOGGER.error("Could not send the Telegram notification: %s", err)
            return False

        _LOGGER.debug("Telegram notification sent to %s", targets)
        return True
