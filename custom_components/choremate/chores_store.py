
from __future__ import annotations
from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store
from .const import STORE_KEY, STORE_VERSION, DAYS

class ChoreStore:
    """Persistente Aufgaben-DB: {person:{tag:[tasks...]}}"""

    def __init__(self, hass: HomeAssistant) -> None:
        self._hass = hass
        self._store = Store(hass, STORE_VERSION, STORE_KEY)
        self.db: dict[str, dict[str, list[str]]] = {}

    async def async_load(self) -> None:
        data = await self._store.async_load()
        self.db = data or {}

        # Sanity: alle Tage anlegen, falls fehlen
        for person in list(self.db.keys()):
            self.db[person] = self.db.get(person) or {}
            for d in DAYS:
                self.db[person].setdefault(d, [])

    async def async_save(self) -> None:
        await self._store.async_save(self.db)

    def add_task(self, person: str, day: str, task: str) -> None:
        self.db.setdefault(person, {})
        self.db[person].setdefault(day, [])
        if task not in self.db[person][day]:
            self.db[person][day].append(task)

    def remove_task(self, person: str, day: str, task: str) -> bool:
        try:
            self.db[person][day].remove(task)
            return True
        except Exception:
            return False

    def list_tasks(self, person: str, day: str) -> list[str]:
        return list(self.db.get(person, {}).get(day, []))
