# -*- coding: utf-8 -*-
"""Sensor platform for Raccolta Rifiuti using calendar event fetching via service call."""

# Creato da domoticafacile.it
import logging
from datetime import timedelta, date, datetime, time

import voluptuous as vol
from homeassistant.components.calendar import (
    DOMAIN as CALENDAR_DOMAIN,
    CalendarEntity,
)
from homeassistant.const import CONF_NAME, EVENT_HOMEASSISTANT_START
from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
import homeassistant.helpers.config_validation as cv
from homeassistant.util import dt as dt_util

from .const import (
    DOMAIN,
    CONF_CALENDAR,
    CONF_SENSOR_NAME,
    CONF_LOOKAHEAD_DAYS,
    DEFAULT_SENSOR_NAME,
    DEFAULT_LOOKAHEAD_DAYS,
    EVENT_TYPE_KEYWORDS,
    DEFAULT_IMAGE,
    IMAGE_BASE_PATH,
    ATTR_EVENT_SUMMARY,
    ATTR_EVENT_START_TIME,
    ATTR_DAYS_REMAINING,
    ATTR_COLLECTION_TYPES,
    STATE_NO_EVENT,
    STATE_UNKNOWN_EVENT,
)

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_CALENDAR): cv.entity_id,
        vol.Optional(CONF_NAME, default=DEFAULT_SENSOR_NAME): cv.string,
        vol.Optional(CONF_LOOKAHEAD_DAYS, default=DEFAULT_LOOKAHEAD_DAYS): cv.positive_int,
    }
)

async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the Raccolta Rifiuti sensor platform."""
    calendar_entity_id = config[CONF_CALENDAR]
    sensor_name = config[CONF_NAME]
    lookahead_days = config[CONF_LOOKAHEAD_DAYS]

    _LOGGER.debug("Setting up Raccolta Rifiuti sensor for calendar: %s", calendar_entity_id)

    async def _async_finalize_setup(_event=None) -> None:
        """Finalize setup after calendar entity might be ready."""
        _LOGGER.debug("Attempting to finalize Raccolta Rifiuti sensor setup.")
        if hass.states.get(calendar_entity_id) is None:
            _LOGGER.error(
                "Calendar entity %s STILL not found after Home Assistant start. "
                "Please check your configuration and calendar integration.",
                calendar_entity_id,
            )
            return

        _LOGGER.info("Calendar entity %s found. Adding Raccolta Rifiuti sensor.", calendar_entity_id)
        sensor = RaccoltaRifiutiSensor(hass, sensor_name, calendar_entity_id, lookahead_days)
        async_add_entities([sensor], True)

    if hass.states.get(calendar_entity_id) is not None:
        _LOGGER.debug("Calendar entity %s found immediately.", calendar_entity_id)
        await _async_finalize_setup()
    else:
        _LOGGER.warning(
            "Calendar entity %s not found immediately. "
            "Will attempt setup again after Home Assistant starts.",
            calendar_entity_id,
        )
        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_START, _async_finalize_setup)

class RaccoltaRifiutiSensor(SensorEntity):
    """Representation of a Raccolta Rifiuti Sensor."""

    def __init__(
        self,
        hass: HomeAssistant,
        name: str,
        calendar_entity_id: str,
        lookahead_days: int,
    ):
        """Initialize the sensor."""
        self.hass = hass
        self._name = name
        self._calendar_entity_id = calendar_entity_id
        self._lookahead_days = lookahead_days

        self._attr_unique_id = f"{DOMAIN}_{calendar_entity_id}_next_collection"
        self._attr_icon = "mdi:trash-can-outline"

        self._state = STATE_NO_EVENT
        self._attributes = self._default_attributes()
        self._entity_picture_path = f"{IMAGE_BASE_PATH}{DEFAULT_IMAGE}"

    def _default_attributes(self) -> dict:
        """Return default attributes."""
        return {
            ATTR_EVENT_SUMMARY: None,
            ATTR_EVENT_START_TIME: None,
            ATTR_DAYS_REMAINING: None,
            ATTR_COLLECTION_TYPES: [],
            "description": None,
            "location": None,
        }

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self) -> str:
        """Return the state of the sensor (tipi di raccolta combinati)."""
        return self._state

    @property
    def extra_state_attributes(self) -> dict:
        """Return the state attributes."""
        return self._attributes

    @property
    def entity_picture(self) -> str | None:
        """Return the entity picture."""
        return self._entity_picture_path

    async def async_update(self) -> None:
        """Fetch new state data for the sensor using the calendar.get_events service."""
        _LOGGER.debug("Updating Raccolta Rifiuti sensor by calling calendar.get_events for %s", self._calendar_entity_id)

        calendar_entity_state = self.hass.states.get(self._calendar_entity_id)
        if calendar_entity_state is None:
            _LOGGER.warning("Calendar entity %s not found during update.", self._calendar_entity_id)
            self._state = "Calendario Non Trovato"
            self._attributes = self._default_attributes()
            self._entity_picture_path = f"{IMAGE_BASE_PATH}{DEFAULT_IMAGE}"
            return

        start_date = dt_util.start_of_local_day()  # Inizia da mezzanotte locale
        # Modifica per calcolare la fine del giorno
        end_date = dt_util.start_of_local_day(start_date + timedelta(days=1)) - timedelta(seconds=1)
        _LOGGER.debug("Fetching events between %s and %s", start_date.isoformat(), end_date.isoformat())

        try:
            service_data = {
                "entity_id": self._calendar_entity_id,
                "start_date_time": start_date.isoformat(),
                "end_date_time": end_date.isoformat(),
            }

            response = await self.hass.services.async_call(
                CALENDAR_DOMAIN,
                "get_events",
                service_data,
                blocking=True,
                return_response=True,
            )

            calendar_events = []
            if response and self._calendar_entity_id in response:
                calendar_events_response = response[self._calendar_entity_id]
                if isinstance(calendar_events_response, dict) and "events" in calendar_events_response:
                    calendar_events = calendar_events_response["events"]
                elif isinstance(calendar_events_response, list):
                    calendar_events = calendar_events_response
                else:
                    _LOGGER.debug("Response format for %s doesn't contain a list or 'events' dict: %s", self._calendar_entity_id, response)

            elif isinstance(response, dict) and "events" in response:
                calendar_events = response["events"]
            else:
                _LOGGER.debug("No events found or unexpected response structure from calendar.get_events for %s: %s", self._calendar_entity_id, response)

        except Exception as e:
            _LOGGER.error(
                "Error calling calendar.get_events service for %s: %s",
                self._calendar_entity_id, e, exc_info=True
            )
            self._state = "Errore Servizio Calendario"
            self._attributes = self._default_attributes()
            self._entity_picture_path = f"{IMAGE_BASE_PATH}{DEFAULT_IMAGE}"
            return

        _LOGGER.debug("Found %d raw events for %s via service call", len(calendar_events), self._calendar_entity_id)

        events_on_current_date = []
        today = dt_util.now().date()

        for event in calendar_events:
            try:
                start_val = event.get('start')
                event_start_dt = None

                if isinstance(start_val, str):
                    if 'T' in start_val:
                        parsed_dt = dt_util.parse_datetime(start_val)
                        if parsed_dt:
                            event_start_dt = dt_util.as_local(parsed_dt)
                    else:
                        parsed_date = dt_util.parse_date(start_val)
                        if parsed_date:
                            event_start_dt = dt_util.start_of_local_day(parsed_date)

                elif isinstance(start_val, datetime):
                    event_start_dt = dt_util.as_local(start_val)
                elif isinstance(start_val, date):
                    event_start_dt = dt_util.start_of_local_day(start_val)

                if event_start_dt is None:
                    _LOGGER.warning("Could not parse start time for event, skipping: %s", event)
                    continue

                event_date = event_start_dt.date()

                if event_date == today:
                    processed_event = {
                        'summary': event.get('summary') or event.get('title', ''),
                        'start': event_start_dt,
                        'end': event.get('end'),
                        'location': event.get('location'),
                        'description': event.get('description')
                    }
                    events_on_current_date.append(processed_event)
                    _LOGGER.debug("Adding event '%s' on %s to process list", processed_event['summary'], event_date)

            except (KeyError, TypeError, ValueError) as e:
                _LOGGER.warning("Could not process event data, skipping. Error: %s, Event: %s", e, event)
                continue

        if not events_on_current_date:
            _LOGGER.debug("No collection events found for today.")
            self._state = STATE_NO_EVENT
            self._attributes = self._default_attributes()
            self._entity_picture_path = f"{IMAGE_BASE_PATH}{DEFAULT_IMAGE}"
            return

        found_types = set()
        found_images = set()
        event_summaries = []
        first_event_start_iso = None
        first_event_description = None
        first_event_location = None

        sorted_keywords = sorted(EVENT_TYPE_KEYWORDS.keys(), key=len, reverse=True)

        for idx, event in enumerate(events_on_current_date):
            event_summary = event.get('summary', '').lower().strip()
            if not event_summary:
                _LOGGER.debug("Skipping event with empty summary: %s", event)
                continue

            original_summary = event.get('summary', '')
            event_summaries.append(original_summary)

            if idx == 0:
                try:
                    first_event_start_iso = event['start'].isoformat()
                    first_event_description = event.get('description')
                    first_event_location = event.get('location')
                except Exception as e:
                    _LOGGER.warning("Could not format start time or get details for first event: %s", e)
                    first_event_start_iso = today.isoformat()

            matched_this_event = False
            summary_for_check = f" {event_summary} "

            for keyword in sorted_keywords:
                if f" {keyword} " in summary_for_check or \
                    event_summary.startswith(keyword + " ") or \
                    event_summary.endswith(" " + keyword) or \
                    event_summary == keyword:

                    type_name = ""
                    image_file = EVENT_TYPE_KEYWORDS.get(keyword, DEFAULT_IMAGE)

                    if keyword in ["indifferenziata", "secco", "rifiuto secco", "indifferenziato"]:
                        type_name = "Indifferenziata"
                    elif keyword in ["umido", "organico"]:
                        type_name = "Umido"
                    elif keyword in ["carta", "cartone"]:
                        type_name = "Carta"
                    elif keyword == "plastica":
                        type_name = "Plastica"
                    elif keyword == "vetro":
                        type_name = "Vetro"
                    else:
                        type_name = keyword.capitalize()

                    if type_name:
                        _LOGGER.debug("Keyword '%s' matched in summary '%s'. Type: %s, Image: %s",
                                      keyword, original_summary, type_name, image_file)
                        found_types.add(type_name)
                        if image_file != DEFAULT_IMAGE:
                            found_images.add(image_file)
                        matched_this_event = True
                        break

            if not matched_this_event:
                _LOGGER.warning("No keyword matched for event summary: '%s'. Adding as unknown.", original_summary)
                found_types.add(STATE_UNKNOWN_EVENT)

        sorted_types = sorted([t for t in found_types if t != STATE_UNKNOWN_EVENT])
        if STATE_UNKNOWN_EVENT in found_types:
            sorted_types.append(STATE_UNKNOWN_EVENT)

        self._state = ", ".join(sorted_types)
        if len(self._state) > 255:
            self._state = self._state[:252] + "..."

        days_remaining = 0  # sempre 0 per gli eventi del giorno corrente

        self._attributes = {
            ATTR_EVENT_SUMMARY: ", ".join(event_summaries)[:1024],
            ATTR_EVENT_START_TIME: first_event_start_iso,
            ATTR_DAYS_REMAINING: days_remaining,
            ATTR_COLLECTION_TYPES: sorted_types,
            "description": first_event_description,
            "location": first_event_location,
        }

        sorted_images = sorted(list(found_images))
        if sorted_images:
            self._entity_picture_path = f"{IMAGE_BASE_PATH}{sorted_images[0]}"
        else:
            self._entity_picture_path = f"{IMAGE_BASE_PATH}{DEFAULT_IMAGE}"

        _LOGGER.debug(
            "Sensor state updated via service: State='{state}', Days={days}, Types={types}, Picture='{pic}'".format(
                state=self._state,
                days=days_remaining,
                types=sorted_types,
                pic=self._entity_picture_path
            )
        )
        _LOGGER.debug("Full attributes: %s", self._attributes)