# -*- coding: utf-8 -*-
"""Config flow and options flow for Raccolta Rifiuti."""

# Creato da domoticafacile.it
from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry, ConfigFlow, ConfigFlowResult, OptionsFlow
from homeassistant.const import CONF_NAME
from homeassistant.core import callback
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.selector import (
    BooleanSelector,
    EntitySelector,
    EntitySelectorConfig,
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
    TextSelector,
    TimeSelector,
)

from .const import (
    CONF_CALENDAR,
    CONF_LANGUAGE,
    CONF_LANGUAGE_AUTO,
    CONF_LOOKAHEAD_DAYS,
    CONF_NOTIFY_EMOJI,
    CONF_NOTIFY_LANGUAGE,
    CONF_NOTIFY_SECOND_ENABLED,
    CONF_NOTIFY_SECOND_TIME,
    CONF_NOTIFY_TIME,
    CONF_NOTIFY_TITLE,
    CONF_TELEGRAM_ENABLED,
    CONF_TELEGRAM_TARGETS,
    DEFAULT_LANGUAGE_OPTION,
    DEFAULT_LOOKAHEAD_DAYS,
    DEFAULT_NOTIFY_SECOND_TIME,
    DEFAULT_NOTIFY_TIME,
    DEFAULT_TITLE,
    DOMAIN,
    MAX_LOOKAHEAD_DAYS,
    TELEGRAM_DOMAIN,
)
from .localization import STRINGS, SUPPORTED_LANGUAGES, resolve_language

LANGUAGE_SELECTOR = SelectSelector(
    SelectSelectorConfig(
        options=[CONF_LANGUAGE_AUTO, *SUPPORTED_LANGUAGES],
        mode=SelectSelectorMode.DROPDOWN,
        translation_key="language",
    )
)

LOOKAHEAD_SELECTOR = NumberSelector(
    NumberSelectorConfig(
        min=0,
        max=MAX_LOOKAHEAD_DAYS,
        step=1,
        mode=NumberSelectorMode.BOX,
        unit_of_measurement="d",
    )
)

# Defaults of the Telegram options (notifications are off until enabled).
TELEGRAM_DEFAULTS: dict[str, Any] = {
    CONF_TELEGRAM_ENABLED: False,
    CONF_NOTIFY_TIME: DEFAULT_NOTIFY_TIME,
    CONF_NOTIFY_SECOND_ENABLED: False,
    CONF_NOTIFY_SECOND_TIME: DEFAULT_NOTIFY_SECOND_TIME,
    CONF_NOTIFY_LANGUAGE: CONF_LANGUAGE_AUTO,
    CONF_NOTIFY_EMOJI: True,
}


def entry_config(entry: ConfigEntry) -> dict[str, Any]:
    """Return the effective configuration: options override the entry data."""
    return {**entry.data, **entry.options}


def _telegram_notify_entities(hass) -> list[str]:
    """Return the notify entities created by the Telegram bot integration."""
    registry = er.async_get(hass)
    return sorted(
        entry.entity_id
        for entry in registry.entities.values()
        if entry.domain == "notify" and entry.platform == TELEGRAM_DOMAIN
    )


class RaccoltaRifiutiConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle the setup of a Raccolta Rifiuti sensor."""

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> RaccoltaRifiutiOptionsFlow:
        """Return the options flow."""
        return RaccoltaRifiutiOptionsFlow()

    def _default_title(self) -> str:
        language = resolve_language(getattr(self.hass.config, "language", None))
        return STRINGS[language]["default_name"] or DEFAULT_TITLE

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """Ask for the calendar and the basic settings."""
        if user_input is not None:
            calendar = user_input[CONF_CALENDAR]
            await self.async_set_unique_id(calendar)
            self._abort_if_unique_id_configured()

            name = (user_input.get(CONF_NAME) or "").strip()
            data: dict[str, Any] = {
                CONF_CALENDAR: calendar,
                CONF_LOOKAHEAD_DAYS: int(user_input[CONF_LOOKAHEAD_DAYS]),
                CONF_LANGUAGE: user_input[CONF_LANGUAGE],
            }
            if name:
                data[CONF_NAME] = name
            return self.async_create_entry(title=name or self._default_title(), data=data)

        schema = vol.Schema(
            {
                vol.Required(CONF_CALENDAR): EntitySelector(EntitySelectorConfig(domain="calendar")),
                vol.Optional(CONF_NAME): TextSelector(),
                vol.Required(CONF_LOOKAHEAD_DAYS, default=DEFAULT_LOOKAHEAD_DAYS): LOOKAHEAD_SELECTOR,
                vol.Required(CONF_LANGUAGE, default=DEFAULT_LANGUAGE_OPTION): LANGUAGE_SELECTOR,
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema)

    async def async_step_import(self, import_data: dict[str, Any]) -> ConfigFlowResult:
        """Import a sensor defined in configuration.yaml (deprecated)."""
        calendar = import_data[CONF_CALENDAR]
        await self.async_set_unique_id(calendar)
        self._abort_if_unique_id_configured()

        name = (import_data.get(CONF_NAME) or "").strip()
        data: dict[str, Any] = {
            CONF_CALENDAR: calendar,
            CONF_LOOKAHEAD_DAYS: int(import_data.get(CONF_LOOKAHEAD_DAYS, DEFAULT_LOOKAHEAD_DAYS)),
            CONF_LANGUAGE: import_data.get(CONF_LANGUAGE, DEFAULT_LANGUAGE_OPTION),
        }
        if name:
            data[CONF_NAME] = name
        return self.async_create_entry(title=name or self._default_title(), data=data)


class RaccoltaRifiutiOptionsFlow(OptionsFlow):
    """Options: general settings and Telegram notifications."""

    def _save(self, new_values: dict[str, Any]) -> ConfigFlowResult:
        """Merge the new values into the options and finish the flow."""
        return self.async_create_entry(title="", data={**self.config_entry.options, **new_values})

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """Show the menu."""
        return self.async_show_menu(step_id="init", menu_options=["general", "telegram"])

    async def async_step_general(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """General settings: sensor name, look-ahead days, display language."""
        current = entry_config(self.config_entry)

        if user_input is not None:
            # A cleared name means "automatic", and must override a stored one.
            name = (user_input.get(CONF_NAME) or "").strip()
            return self._save(
                {
                    CONF_NAME: name,
                    CONF_LOOKAHEAD_DAYS: int(user_input[CONF_LOOKAHEAD_DAYS]),
                    CONF_LANGUAGE: user_input[CONF_LANGUAGE],
                }
            )

        schema = vol.Schema(
            {
                vol.Optional(CONF_NAME, description={"suggested_value": current.get(CONF_NAME) or ""}): TextSelector(),
                vol.Required(
                    CONF_LOOKAHEAD_DAYS,
                    default=current.get(CONF_LOOKAHEAD_DAYS, DEFAULT_LOOKAHEAD_DAYS),
                ): LOOKAHEAD_SELECTOR,
                vol.Required(
                    CONF_LANGUAGE, default=current.get(CONF_LANGUAGE, DEFAULT_LANGUAGE_OPTION)
                ): LANGUAGE_SELECTOR,
            }
        )
        return self.async_show_form(step_id="general", data_schema=schema)

    async def async_step_telegram(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """Telegram notifications: on/off, recipients, times, message."""
        current = {**TELEGRAM_DEFAULTS, **entry_config(self.config_entry)}
        available = _telegram_notify_entities(self.hass)

        if not available and not current[CONF_TELEGRAM_ENABLED]:
            return self.async_abort(reason="telegram_not_available")

        errors: dict[str, str] = {}
        if user_input is not None:
            enabled = user_input[CONF_TELEGRAM_ENABLED]
            targets = list(user_input.get(CONF_TELEGRAM_TARGETS) or [])
            second_enabled = user_input[CONF_NOTIFY_SECOND_ENABLED]

            if enabled and not targets:
                errors[CONF_TELEGRAM_TARGETS] = "no_targets"
            elif any(target not in available for target in targets):
                errors[CONF_TELEGRAM_TARGETS] = "invalid_target"
            if enabled and second_enabled and user_input[CONF_NOTIFY_SECOND_TIME] == user_input[CONF_NOTIFY_TIME]:
                errors[CONF_NOTIFY_SECOND_TIME] = "same_time"

            if not errors:
                return self._save(
                    {
                        CONF_TELEGRAM_ENABLED: enabled,
                        CONF_TELEGRAM_TARGETS: targets,
                        CONF_NOTIFY_TIME: user_input[CONF_NOTIFY_TIME],
                        CONF_NOTIFY_SECOND_ENABLED: second_enabled,
                        CONF_NOTIFY_SECOND_TIME: user_input[CONF_NOTIFY_SECOND_TIME],
                        CONF_NOTIFY_LANGUAGE: user_input[CONF_NOTIFY_LANGUAGE],
                        CONF_NOTIFY_EMOJI: user_input[CONF_NOTIFY_EMOJI],
                        CONF_NOTIFY_TITLE: (user_input.get(CONF_NOTIFY_TITLE) or "").strip(),
                    }
                )
            # Show the form again with what the user typed.
            current = {**current, **user_input}

        schema = vol.Schema(
            {
                vol.Required(CONF_TELEGRAM_ENABLED, default=current[CONF_TELEGRAM_ENABLED]): BooleanSelector(),
                vol.Optional(
                    CONF_TELEGRAM_TARGETS,
                    description={"suggested_value": current.get(CONF_TELEGRAM_TARGETS) or []},
                ): EntitySelector(
                    EntitySelectorConfig(domain="notify", integration=TELEGRAM_DOMAIN, multiple=True)
                ),
                vol.Required(CONF_NOTIFY_TIME, default=current[CONF_NOTIFY_TIME]): TimeSelector(),
                vol.Required(
                    CONF_NOTIFY_SECOND_ENABLED, default=current[CONF_NOTIFY_SECOND_ENABLED]
                ): BooleanSelector(),
                vol.Required(CONF_NOTIFY_SECOND_TIME, default=current[CONF_NOTIFY_SECOND_TIME]): TimeSelector(),
                vol.Required(CONF_NOTIFY_LANGUAGE, default=current[CONF_NOTIFY_LANGUAGE]): LANGUAGE_SELECTOR,
                vol.Required(CONF_NOTIFY_EMOJI, default=current[CONF_NOTIFY_EMOJI]): BooleanSelector(),
                vol.Optional(
                    CONF_NOTIFY_TITLE,
                    description={"suggested_value": current.get(CONF_NOTIFY_TITLE) or ""},
                ): TextSelector(),
            }
        )
        return self.async_show_form(step_id="telegram", data_schema=schema, errors=errors)
