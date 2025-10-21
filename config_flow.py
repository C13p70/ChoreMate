
"""Config flow for ChoreMate integration."""
from __future__ import annotations
import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_NAME
from homeassistant.helpers import config_validation as cv

_LOGGER = logging.getLogger(__name__)

DOMAIN = "choremate"

CONF_PERSONS = "persons"
CONF_TASKS_PER_DAY = "tasks_per_day"
CONF_AUTO_ENABLED = "auto_enabled"
CONF_AUTO_INTERVAL = "auto_interval"

DEFAULT_TASKS_PER_DAY = 2
DEFAULT_AUTO_ENABLED = True
DEFAULT_AUTO_INTERVAL = 7

# --- TRANSLATIONS ---
TEXTS = {
    "en": {
        "title": "ChoreMate Setup",
        "desc": "Configure your household chore distribution.",
        "persons": "Household members (comma-separated)",
        "tasks_per_day": "Tasks per person/day",
        "auto_enabled": "Automatic reassignment enabled",
        "auto_interval": "Automatic reassignment every (days)",
    },
    "de": {
        "title": "ChoreMate Einrichtung",
        "desc": "Konfiguriere die Verteilung deiner Haushaltsaufgaben.",
        "persons": "Haushaltsmitglieder (durch Komma getrennt)",
        "tasks_per_day": "Aufgaben pro Person/Tag",
        "auto_enabled": "Automatische Neuverteilung aktivieren",
        "auto_interval": "Automatische Neuverteilung alle (Tage)",
    }
}

def get_text(lang: str, key: str) -> str:
    if lang.startswith("de"):
        return TEXTS["de"][key]
    return TEXTS["en"][key]


class ChoreMateConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the config flow for ChoreMate."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        lang = self.hass.config.language
        errors = {}

        if user_input is not None:
            persons = [p.strip() for p in user_input[CONF_PERSONS].split(",") if p.strip()]
            if not persons:
                errors[CONF_PERSONS] = "no_persons"
            else:
                return self.async_create_entry(title="ChoreMate", data=user_input)

        data_schema = vol.Schema({
            vol.Required(CONF_PERSONS): str,
            vol.Required(CONF_TASKS_PER_DAY, default=DEFAULT_TASKS_PER_DAY): int,
            vol.Required(CONF_AUTO_ENABLED, default=DEFAULT_AUTO_ENABLED): bool,
            vol.Required(CONF_AUTO_INTERVAL, default=DEFAULT_AUTO_INTERVAL): int,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "desc": get_text(lang, "desc")
            },
            title=get_text(lang, "title")
        )

    async def async_step_import(self, user_input=None):
        """Support import from configuration.yaml."""
        return await self.async_step_user(user_input)


class ChoreMateOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options for ChoreMate."""

    def __init__(self, config_entry: config_entries.ConfigEntry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage options."""
        lang = self.hass.config.language
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options = self.config_entry.options
        data_schema = vol.Schema({
            vol.Required(CONF_PERSONS, default=options.get(CONF_PERSONS, "")): str,
            vol.Required(CONF_TASKS_PER_DAY, default=options.get(CONF_TASKS_PER_DAY, DEFAULT_TASKS_PER_DAY)): int,
            vol.Required(CONF_AUTO_ENABLED, default=options.get(CONF_AUTO_ENABLED, DEFAULT_AUTO_ENABLED)): bool,
            vol.Required(CONF_AUTO_INTERVAL, default=options.get(CONF_AUTO_INTERVAL, DEFAULT_AUTO_INTERVAL)): int,
        })

        return self.async_show_form(
            step_id="init",
            data_schema=data_schema,
            title=get_text(lang, "title"),
            description_placeholders={"desc": get_text(lang, "desc")}
        )
