"""Initialize the ChoreMate integration."""
from __future__ import annotations

import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up ChoreMate via YAML (deprecated)."""
    _LOGGER.debug("ChoreMate async_setup() called (YAML not supported)")
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up ChoreMate from a config entry."""
    _LOGGER.info("Setting up ChoreMate integration entry: %s", entry.title)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "persons": entry.data.get("persons", "").split(","),
        "tasks_per_day": entry.data.get("tasks_per_day", 2),
        "auto_enabled": entry.data.get("auto_enabled", True),
        "auto_interval": entry.data.get("auto_interval", 7),
    }

    # Placeholder for creating entities/sensors later
    # e.g. await hass.config_entries.async_forward_entry_setup(entry, "sensor")

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Handle removal of an entry."""
    _LOGGER.info("Unloading ChoreMate integration entry: %s", entry.title)
    hass.data[DOMAIN].pop(entry.entry_id, None)
    return True
