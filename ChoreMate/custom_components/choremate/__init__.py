
from __future__ import annotations
import random
from datetime import timedelta
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.dispatcher import async_dispatcher_send

from .const import (
    DOMAIN, CONF_PERSONS, DEFAULT_PERSONS, DAYS,
    SVC_ASSIGN_NOW, SVC_ADD_TASK, SVC_REMOVE_TASK, SVC_LIST_TASKS,
    SIGNAL_UPDATED
)
from .chores_store import ChoreStore

PLATFORMS = ["sensor"]

class ChoreHub:
    """Zentrale Datenhaltung & Logik."""
    def __init__(self, hass: HomeAssistant, persons: list[dict]):
        self.hass = hass
        # persons = [{"name":"Mama","lines":2}, ...]
        self.persons = persons
        # aktuelle Zuweisungen: {(person,day): ["Task1","Task2"]}
        self.assignments: dict[tuple[str,str], list[str]] = {}
        self.store = ChoreStore(hass)

    async def async_setup(self):
        await self.store.async_load()

    async def async_assign_now(self) -> None:
        """Zufällig zuweisen für alle Personen & Tage."""
        for p in self.persons:
            name = p["name"]
            lines = int(p.get("lines", 2))
            for day in DAYS:
                pool = list(self.store.list_tasks(name, day))
                if pool:
                    random.shuffle(pool)
                    # Pool ggf. wiederholen
                    times = (lines + len(pool) - 1) // len(pool)
                    chosen = (pool * times)[:lines]
                else:
                    chosen = [""] * lines
                self.assignments[(name, day)] = chosen
        # Sensoren benachrichtigen
        async_dispatcher_send(self.hass, SIGNAL_UPDATED)

    def get_assignment_text(self, person: str, day: str) -> str:
        return "\n".join(self.assignments.get((person, day), []))

async def async_setup(hass: HomeAssistant, config: ConfigType):
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    persons = entry.data.get(CONF_PERSONS, DEFAULT_PERSONS)
    hub = ChoreHub(hass, persons)
    await hub.async_setup()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = hub

    # Plattformen laden
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Services
    async def _assign_now(call: ServiceCall):
        await hub.async_assign_now()

    async def _add_task(call: ServiceCall):
        person = call.data["person"]; day = call.data["day"]; task = call.data["task"]
        hub.store.add_task(person, day, task)
        await hub.store.async_save()

    async def _remove_task(call: ServiceCall):
        person = call.data["person"]; day = call.data["day"]; task = call.data["task"]
        ok = hub.store.remove_task(person, day, task)
        await hub.store.async_save()
        if not ok:
            raise ValueError("Task nicht gefunden")

    async def _list_tasks(call: ServiceCall):
        person = call.data["person"]; day = call.data["day"]
        tasks = hub.store.list_tasks(person, day)
        hass.bus.async_fire(f"{DOMAIN}_list_tasks", {
            "person": person, "day": day, "tasks": tasks
        })

    hass.services.async_register(DOMAIN, SVC_ASSIGN_NOW, _assign_now)
    hass.services.async_register(DOMAIN, SVC_ADD_TASK, _add_task)
    hass.services.async_register(DOMAIN, SVC_REMOVE_TASK, _remove_task)
    hass.services.async_register(DOMAIN, SVC_LIST_TASKS, _list_tasks)

    # Beispiel: wöchentliche Neuverteilung – alle 7 Tage
    async def _weekly(_now):
        await hub.async_assign_now()
    async_track_time_interval(hass, _weekly, timedelta(days=7))

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
