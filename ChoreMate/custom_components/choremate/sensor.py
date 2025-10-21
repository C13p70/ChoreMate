
from __future__ import annotations
from homeassistant.core import callback
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN, CONF_PERSONS, DEFAULT_PERSONS, DAYS, SIGNAL_UPDATED

async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities):
    hub = hass.data[DOMAIN][entry.entry_id]
    persons = entry.data.get(CONF_PERSONS, DEFAULT_PERSONS)
    entities = []
    for p in persons:
        name = p["name"]
        for day in DAYS:
            entities.append(ChoreSensor(hub, name, day, entry.entry_id))
    async_add_entities(entities, True)

class ChoreSensor(SensorEntity):
    _attr_icon = "mdi:clipboard-text"

    def __init__(self, hub, person: str, day: str, entry_id: str) -> None:
        self._hub = hub
        self._person = person
        self._day = day
        self._entry_id = entry_id
        self._attr_unique_id = f"{entry_id}_{person}_{day}".lower().replace(" ","_")
        self._attr_name = f"{person} {day}"

    async def async_added_to_hass(self) -> None:
        @callback
        def _updated(*_):
            self.async_write_ha_state()
        self.async_on_remove(
            async_dispatcher_connect(self.hass, SIGNAL_UPDATED, _updated)
        )

    @property
    def native_value(self):
        return self._hub.get_assignment_text(self._person, self._day)

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(identifiers={(DOMAIN, self._entry_id)}, name="ChoreMate")
