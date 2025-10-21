"""Config flow for ChoreMate integration."""
from __future__ import annotations

import logging
import voluptuous as vol
from homeassistant import config_entries

_LOGGER = logging.getLogger(__name__)

DOMAIN = "choremate"

CONF_PERSONS = "persons"
CONF_TASKS_PER_DAY = "tasks_per_day"
CONF_AUTO_ENABLED = "auto_enabled"
CONF_AUTO_INTERVAL = "auto_interval"

DEFAULT_TASKS_PER_DAY = 2
DEFAULT_AUTO_ENABLED = True
DEFAULT_AUTO_INTERVAL = 7


def _get_lang(hass):
    """Try to detect UI language safely."""
    try:
        return getattr(hass.config, "language", "en")
    except Exception:
        return "en"


def _t(lang: str, key: str) -> str:
    """Simple translation system."""
    text = {
        "en": {
            "title": "ChoreMate Setup",
            "desc": "Configure your household chore distribution.",
            "persons": "Household members (comma-separated)",
            "tasks_per_day": "Tasks per person/day",
            "auto_enabled": "Enable automatic reassignment",
            "auto_interval": "Automatic reassignment every (days)",
        },
        "de": {
            "title": "ChoreMate Einrichtung",
            "desc": "Konfiguriere die Verteilung deiner Haushaltsaufgaben.",
            "persons": "Haushaltsmitglieder (durch Komma getrennt)",
            "tasks_per_day": "Aufgaben pro Person/Tag",
            "auto_enabled": "Automatische Neuverteilung aktivieren",
            "auto_interval": "Automatische Neuverteilung alle (Tage)",
        },
    }
    return text["de" if lang.startswith("de") else "en"].get(key, key)


class ChoreMateConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the config flow for ChoreMate."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial setup."""
        lang = _get_lang(self.hass)
        errors = {}

        if user_input is not None:
            persons = [p.strip() for p in user_input[CONF_PERSONS].split(",") if p.strip()]
            if not persons:
                errors[CONF_PERSONS] = "no_persons"
            else:
                return self.async_create_entry(title="ChoreMate", data=user_input)

        schema = vol.Schema({
            vol.Required(CONF_PERSONS): str,
            vol.Required(CONF_TASKS_PER_DAY, default=DEFAULT_TASKS_PER_DAY): int,
            vol.Required(CONF_AUTO_ENABLED, default=DEFAULT_AUTO_ENABLED): bool,
            vol.Required(CONF_AUTO_INTERVAL, default=DEFAULT_AUTO_INTERVAL): int,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
            description_placeholders={},  # leer lassen!
            title=_t(lang, "title"),
            description=_t(lang, "desc"),
        )

    async def async_step_import(self, user_input=None):
        """Handle import from configuration.yaml."""
        return await self.async_step_user(user_input)


class ChoreMateOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options for ChoreMate."""

    def __init__(self, config_entry: config_entries.ConfigEntry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage options."""
        lang = _get_lang(self.hass)
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options = self.config_entry.options
        schema = vol.Schema({
            vol.Required(CONF_PERSONS, default=options.get(CONF_PERSONS, "")): str,
            vol.Required(CONF_TASKS_PER_DAY, default=options.get(CONF_TASKS_PER_DAY, DEFAULT_TASKS_PER_DAY)): int,
            vol.Required(CONF_AUTO_ENABLED, default=options.get(CONF_AUTO_ENABLED, DEFAULT_AUTO_ENABLED)): bool,
            vol.Required(CONF_AUTO_INTERVAL, default=options.get(CONF_AUTO_INTERVAL, DEFAULT_AUTO_INTERVAL)): int,
        })

        return self.async_show_form(
            step_id="init",
            data_schema=schema,
            title=_t(lang, "title"),
            description=_t(lang, "desc"),
        )
